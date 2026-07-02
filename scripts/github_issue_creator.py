#!/usr/bin/env python3
"""
GitHub Issue Creator for Recursive TODO Resolution

This module provides GitHub API integration for automatic issue creation
as part of the recursive TODO resolution system.

Author: OpenCog Unified Cognitive Enhancement System
"""

import os
from typing import Any

import requests


class GitHubIssueCreator:
    """Handles automatic GitHub issue creation for TODO batches"""

    def __init__(self, repo_owner: str = "OzCog", repo_name: str = "opencog-unified"):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.base_url = "https://api.github.com"

    def create_todo_batch_issue(self, batch_content: str, batch_number: int) -> dict[Any, Any] | None:
        """Create a GitHub issue for a TODO batch"""

        if not self.github_token:
            print("⚠️  No GITHUB_TOKEN found in environment. Skipping automatic issue creation.")
            print("   To enable automatic issue creation, set GITHUB_TOKEN environment variable.")
            return None

        # Extract title from content
        lines = batch_content.split("\n")
        title = lines[0].strip("# ")

        # Prepare issue data
        issue_data = {
            "title": title,
            "body": batch_content,
            "labels": ["todo-resolution", "cognitive-enhancement", "recursive-attention", f"batch-{batch_number}"],
            "assignees": [],  # Can be configured
        }

        # Create the issue
        url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/issues"
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json",
        }

        try:
            print(f"🚀 Creating GitHub issue for Batch {batch_number}...")
            response = requests.post(url, headers=headers, json=issue_data)
            response.raise_for_status()

            issue = response.json()
            print(f"✅ Created GitHub issue #{issue['number']}: {issue['html_url']}")
            return issue

        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to create GitHub issue: {e}")
            if hasattr(e, "response") and e.response is not None:
                print(f"   Response: {e.response.text}")
            return None

    def update_issue_with_completion(self, issue_number: int, todo_key: str, pr_link: str) -> bool:
        """Update an issue to mark a TODO as completed"""

        if not self.github_token:
            return False

        # Get current issue content
        url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/issues/{issue_number}"
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json",
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            issue = response.json()

            # Update the issue body to mark the TODO as completed
            updated_body = issue["body"].replace(f"**[ ] {todo_key}", f"**[x] {todo_key} ✅ [Resolved]({pr_link})")

            # Update the issue
            update_data = {"body": updated_body}
            response = requests.patch(url, headers=headers, json=update_data)
            response.raise_for_status()

            print(f"✅ Updated issue #{issue_number} with completion of {todo_key}")
            return True

        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to update GitHub issue: {e}")
            return False

    def create_pr_stub(self, todo_item: str, implementation_guidance: str) -> str | None:
        """Create a PR stub/draft for a TODO item (future enhancement)"""
        # This could be implemented to auto-create PR drafts
        # For now, just return a suggested branch name
        file_part = todo_item.split(":", maxsplit=1)[0]
        safe_name = file_part.replace("/", "-").replace(".", "-")
        return f"fix-todo-{safe_name}"


def main():
    """Test the GitHub issue creator"""
    creator = GitHubIssueCreator()

    # Test with a sample batch content
    sample_content = """# Test TODO Resolution Batch

## Objective
Testing GitHub integration

**1. [ ] test/file.cc:123 (HIGH, Feature)**
   - Sample TODO item for testing
   - **Action:** Test implementation
   - **Test:** Validate functionality
"""

    issue = creator.create_todo_batch_issue(sample_content, 999)
    if issue:
        print(f"Test issue created: {issue['html_url']}")
    else:
        print("No GitHub token available for testing")


if __name__ == "__main__":
    main()
