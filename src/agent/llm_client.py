"""LLM client wrapper supporting multiple AI providers."""

import os
from typing import Optional, List, Dict, Any
import openai
from anthropic import Anthropic


class LLMClient:
    """Unified client for multiple LLM providers."""

    def __init__(self, provider: str = "perplexity", model: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initialize LLM client.

        Args:
            provider: AI provider (anthropic, openai, or perplexity)
            model: Model name to use
            api_key: API key for the provider
        """
        self.provider = provider.lower()
        self.model = model
        self.api_key = api_key

        if self.provider == "anthropic":
            self.client = Anthropic(api_key=self.api_key)
        elif self.provider in ["openai", "perplexity"]:
            # Perplexity uses OpenAI-compatible API
            if self.provider == "perplexity":
                self.client = openai.OpenAI(
                    api_key=self.api_key,
                    base_url="https://api.perplexity.ai"
                )
            else:
                self.client = openai.OpenAI(api_key=self.api_key)
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4000,
    ) -> str:
        """
        Generate text using the configured LLM.

        Args:
            prompt: User prompt
            system_prompt: System prompt (optional)
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate

        Returns:
            Generated text
        """
        try:
            if self.provider == "anthropic":
                return self._generate_anthropic(prompt, system_prompt, temperature, max_tokens)
            elif self.provider in ["openai", "perplexity"]:
                return self._generate_openai(prompt, system_prompt, temperature, max_tokens)
        except Exception as e:
            raise RuntimeError(f"Error generating response: {e}")

    def _generate_anthropic(
        self,
        prompt: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
    ) -> str:
        """Generate using Anthropic API."""
        messages = [{"role": "user", "content": prompt}]

        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        if system_prompt:
            kwargs["system"] = system_prompt

        response = self.client.messages.create(**kwargs)
        return response.content[0].text

    def _generate_openai(
        self,
        prompt: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
    ) -> str:
        """Generate using OpenAI or Perplexity API."""
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        return response.choices[0].message.content

    def generate_with_search(self, query: str, temperature: float = 0.7) -> Dict[str, Any]:
        """
        Generate response with web search (Perplexity-specific feature).

        Args:
            query: Search query
            temperature: Sampling temperature

        Returns:
            Dictionary with response and citations
        """
        if self.provider != "perplexity":
            raise NotImplementedError("Search feature is only available with Perplexity")

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": query}],
                temperature=temperature,
            )

            # Extract response and citations
            result = {
                "content": response.choices[0].message.content,
                "citations": getattr(response, "citations", []),
            }

            return result
        except Exception as e:
            raise RuntimeError(f"Error in search-enhanced generation: {e}")
