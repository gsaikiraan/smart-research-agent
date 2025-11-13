"""Main research agent orchestrator."""

from typing import Dict, Any, List
from pathlib import Path
from datetime import datetime

from ..utils.config import Config
from .llm_client import LLMClient
from ..search.web_search import WebSearcher
from ..storage.database import ResearchDatabase


class ResearchAgent:
    """AI-powered research agent."""

    def __init__(self, config: Config):
        """
        Initialize research agent.

        Args:
            config: Configuration object
        """
        self.config = config

        # Initialize components
        self.llm = LLMClient(
            provider=config.ai_provider,
            model=config.get_model(),
            api_key=config.get_api_key(),
        )
        self.searcher = WebSearcher(engine=config.search_engine)
        self.db = ResearchDatabase(config.database_path)

    def research(
        self, topic: str, depth: str = "standard", max_sources: int = 5
    ) -> Dict[str, Any]:
        """
        Conduct research on a topic.

        Args:
            topic: Research topic
            depth: Research depth (quick, standard, deep)
            max_sources: Maximum number of sources to analyze

        Returns:
            Research results dictionary
        """
        # Create research session
        session_id = self.db.create_session(topic, depth)

        print(f"📚 Starting research session {session_id} on: {topic}")

        # Step 1: Generate research questions
        print("\n🤔 Generating research questions...")
        research_questions = self._generate_research_questions(topic, depth)
        print(f"   Generated {len(research_questions)} research questions")

        # Step 2: Search and collect sources
        print("\n🔍 Searching for sources...")
        sources = self._collect_sources(topic, research_questions, max_sources)
        print(f"   Found {len(sources)} relevant sources")

        # Save sources to database
        for source in sources:
            self.db.add_source(
                session_id,
                source["title"],
                source["url"],
                source["content"],
                source.get("relevance", 0.0),
            )

        # Step 3: Analyze sources and extract findings
        print("\n📊 Analyzing sources and extracting findings...")
        findings = self._analyze_sources(topic, sources, research_questions)
        print(f"   Extracted {len(findings)} key findings")

        # Save findings
        for finding in findings:
            self.db.add_finding(
                session_id, finding["text"], finding.get("source_ids", [])
            )

        # Step 4: Synthesize final report
        print("\n✍️  Synthesizing final report...")
        report = self._generate_report(topic, findings, sources)

        # Save report
        report_path = self._save_report(session_id, topic, report)
        print(f"   Report saved to: {report_path}")

        # Complete session
        self.db.complete_session(session_id, report["summary"], str(report_path))

        return {
            "session_id": session_id,
            "topic": topic,
            "report": report,
            "report_path": report_path,
            "sources": sources,
            "findings": findings,
        }

    def _generate_research_questions(self, topic: str, depth: str) -> List[str]:
        """Generate research questions for the topic."""
        num_questions = {"quick": 3, "standard": 5, "deep": 8}.get(depth, 5)

        prompt = f"""You are a research assistant. Generate {num_questions} specific research questions to thoroughly investigate the following topic:

Topic: {topic}

Generate focused, specific questions that will help gather comprehensive information about this topic. Return only the questions, one per line, numbered."""

        try:
            response = self.llm.generate(
                prompt, system_prompt="You are a helpful research assistant.", temperature=0.7
            )

            # Parse questions
            questions = [
                line.strip().lstrip("0123456789.)-").strip()
                for line in response.split("\n")
                if line.strip() and any(c.isalpha() for c in line)
            ]

            return questions[:num_questions]
        except Exception as e:
            print(f"Error generating research questions: {e}")
            return [topic]  # Fallback to just the topic

    def _collect_sources(
        self, topic: str, questions: List[str], max_sources: int
    ) -> List[Dict[str, Any]]:
        """Collect and extract content from web sources."""
        sources = []
        queries = [topic] + questions[:3]  # Use topic + top 3 questions

        for query in queries:
            if len(sources) >= max_sources:
                break

            search_results = self.searcher.search(query, max_results=3)

            for result in search_results:
                if len(sources) >= max_sources:
                    break

                # Extract full content
                content = self.searcher.extract_content(result["url"])

                if content:
                    sources.append({
                        "title": result["title"],
                        "url": result["url"],
                        "snippet": result["snippet"],
                        "content": content,
                        "query": query,
                    })

        return sources

    def _analyze_sources(
        self, topic: str, sources: List[Dict[str, Any]], questions: List[str]
    ) -> List[Dict[str, Any]]:
        """Analyze sources and extract key findings."""
        findings = []

        # Prepare context
        sources_text = "\n\n".join(
            [
                f"Source {i+1}: {s['title']}\nURL: {s['url']}\nContent: {s['content'][:1500]}..."
                for i, s in enumerate(sources)
            ]
        )

        prompt = f"""You are analyzing research sources about: {topic}

Research Questions:
{chr(10).join(f"{i+1}. {q}" for i, q in enumerate(questions))}

Sources:
{sources_text}

Based on these sources, extract 5-10 key findings. For each finding:
1. Summarize the key point
2. Note which sources support it
3. Assess confidence level

Format each finding as:
FINDING: [Your finding]
SOURCES: [Source numbers]
CONFIDENCE: [High/Medium/Low]"""

        try:
            response = self.llm.generate(
                prompt,
                system_prompt="You are a thorough research analyst.",
                temperature=0.5,
                max_tokens=2000,
            )

            # Parse findings
            current_finding = {}
            for line in response.split("\n"):
                line = line.strip()
                if line.startswith("FINDING:"):
                    if current_finding:
                        findings.append(current_finding)
                    current_finding = {"text": line.replace("FINDING:", "").strip()}
                elif line.startswith("SOURCES:"):
                    current_finding["sources"] = line.replace("SOURCES:", "").strip()
                elif line.startswith("CONFIDENCE:"):
                    current_finding["confidence"] = line.replace("CONFIDENCE:", "").strip()

            if current_finding:
                findings.append(current_finding)

        except Exception as e:
            print(f"Error analyzing sources: {e}")

        return findings

    def _generate_report(
        self, topic: str, findings: List[Dict[str, Any]], sources: List[Dict[str, Any]]
    ) -> Dict[str, str]:
        """Generate final research report."""
        findings_text = "\n".join(
            [f"{i+1}. {f['text']}" for i, f in enumerate(findings)]
        )

        prompt = f"""Create a comprehensive research report on: {topic}

Key Findings:
{findings_text}

Generate a well-structured report with:
1. Executive Summary (2-3 paragraphs)
2. Detailed Analysis (organized by themes)
3. Key Takeaways (bullet points)
4. Conclusion

Write in a clear, professional style."""

        try:
            report_content = self.llm.generate(
                prompt,
                system_prompt="You are a professional research writer.",
                temperature=0.6,
                max_tokens=3000,
            )

            # Extract summary (first paragraph)
            summary = report_content.split("\n\n")[0] if report_content else ""

            return {"content": report_content, "summary": summary}
        except Exception as e:
            print(f"Error generating report: {e}")
            return {"content": "Error generating report", "summary": ""}

    def _save_report(self, session_id: int, topic: str, report: Dict[str, str]) -> Path:
        """Save report to file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_topic = "".join(c for c in topic if c.isalnum() or c in " -_")[:50]
        filename = f"{timestamp}_{safe_topic}.md"

        report_path = self.config.report_output_dir / filename
        report_path.parent.mkdir(parents=True, exist_ok=True)

        with open(report_path, "w", encoding="utf-8") as f:
            f.write(f"# Research Report: {topic}\n\n")
            f.write(f"**Session ID:** {session_id}\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")
            f.write(report["content"])

        return report_path
