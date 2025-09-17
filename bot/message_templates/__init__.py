"""
Fast Track Academy - Message Templates

This module provides customizable message templates for the DutyBot
to use across different contexts and interactions.
"""

import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import random

logger = logging.getLogger(__name__)


@dataclass
class MessageTemplate:
    """Data class representing a message template."""
    template_id: str
    category: str
    content: str
    placeholders: List[str]
    usage_count: int = 0
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


class TemplateManager:
    """Manages message templates for the DutyBot."""
    
    def __init__(self):
        self.templates: Dict[str, MessageTemplate] = {}
        self.categories: Dict[str, List[str]] = {}
        self._load_default_templates()
    
    def _load_default_templates(self) -> None:
        """Load default message templates."""
        default_templates = [
            # Greeting templates
            MessageTemplate(
                template_id="greeting_001",
                category="greeting",
                content="Hello {name}! Welcome to Fast Track Academy. I'm {bot_name}, your virtual learning assistant.",
                placeholders=["name", "bot_name"]
            ),
            MessageTemplate(
                template_id="greeting_002",
                category="greeting",
                content="Hi there! I'm {bot_name}, ready to help you navigate the academy. What would you like to explore today?",
                placeholders=["bot_name"]
            ),
            MessageTemplate(
                template_id="greeting_003",
                category="greeting",
                content="Greetings, {name}! Fast Track Academy is here to accelerate your learning journey. How can I assist you?",
                placeholders=["name"]
            ),
            
            # Help templates
            MessageTemplate(
                template_id="help_001",
                category="help",
                content="I can help you with: course navigation, achievement tracking, resource access, and answering academy-related questions. What specific area interests you?",
                placeholders=[]
            ),
            MessageTemplate(
                template_id="help_002",
                category="help",
                content="Need assistance? I'm here to guide you through the academy platform, help with assignments, or connect you with learning resources. Just ask!",
                placeholders=[]
            ),
            MessageTemplate(
                template_id="help_003",
                category="help",
                content="Hello {name}! I can assist with course materials, track your progress, explain academy features, or answer questions about {topic}. What would you like to know?",
                placeholders=["name", "topic"]
            ),
            
            # Course-related templates
            MessageTemplate(
                template_id="course_001",
                category="course",
                content="The {course_name} course includes {module_count} modules covering {topics}. Your current progress is {progress}%. Keep up the great work!",
                placeholders=["course_name", "module_count", "topics", "progress"]
            ),
            MessageTemplate(
                template_id="course_002",
                category="course",
                content="Ready to continue with {course_name}? You're currently on module {current_module}. The next topic is {next_topic}.",
                placeholders=["course_name", "current_module", "next_topic"]
            ),
            
            # Achievement templates
            MessageTemplate(
                template_id="achievement_001",
                category="achievement",
                content="Congratulations {name}! You've earned the '{achievement_name}' badge for {accomplishment}. You're making excellent progress! 🏆",
                placeholders=["name", "achievement_name", "accomplishment"]
            ),
            MessageTemplate(
                template_id="achievement_002",
                category="achievement",
                content="Amazing work! You've completed {milestone} and unlocked {reward}. Your dedication to learning is inspiring! ⭐",
                placeholders=["milestone", "reward"]
            ),
            
            # Encouragement templates
            MessageTemplate(
                template_id="encouragement_001",
                category="encouragement",
                content="You're doing fantastic, {name}! Remember, every expert was once a beginner. Keep pushing forward! 💪",
                placeholders=["name"]
            ),
            MessageTemplate(
                template_id="encouragement_002",
                category="encouragement",
                content="Learning is a journey, not a destination. You're making great progress in {subject}. Stay curious and keep exploring!",
                placeholders=["subject"]
            ),
            
            # Social media templates
            MessageTemplate(
                template_id="social_001",
                category="social",
                content="🚀 Fast Track Academy Update: {update_content} Join our learning community! #FastTrackAcademy #Learning #Education",
                placeholders=["update_content"]
            ),
            MessageTemplate(
                template_id="social_002",
                category="social",
                content="📚 Daily Learning Tip: {tip_content} What's your favorite study technique? Share with #StudyTips #FastTrackAcademy",
                placeholders=["tip_content"]
            ),
            
            # Error/Support templates
            MessageTemplate(
                template_id="error_001",
                category="error",
                content="I apologize, but I didn't quite understand that. Could you please rephrase your question or try asking about {suggested_topic}?",
                placeholders=["suggested_topic"]
            ),
            MessageTemplate(
                template_id="support_001",
                category="support",
                content="If you need technical support, please contact our support team at {support_email} or visit the help section in your dashboard.",
                placeholders=["support_email"]
            )
        ]
        
        for template in default_templates:
            self.add_template(template)
        
        logger.info(f"Loaded {len(default_templates)} default templates")
    
    def add_template(self, template: MessageTemplate) -> None:
        """Add a template to the manager."""
        self.templates[template.template_id] = template
        
        # Update category index
        if template.category not in self.categories:
            self.categories[template.category] = []
        self.categories[template.category].append(template.template_id)
    
    def get_template(self, template_id: str) -> Optional[MessageTemplate]:
        """Get a specific template by ID."""
        return self.templates.get(template_id)
    
    def get_templates_by_category(self, category: str) -> List[MessageTemplate]:
        """Get all templates in a specific category."""
        template_ids = self.categories.get(category, [])
        return [self.templates[tid] for tid in template_ids if tid in self.templates]
    
    def generate_message(self, template_id: str, **kwargs) -> str:
        """Generate a message from a template with provided parameters."""
        template = self.get_template(template_id)
        if not template:
            return f"Template {template_id} not found."
        
        try:
            # Update usage count
            template.usage_count += 1
            
            # Replace placeholders
            message = template.content
            for placeholder in template.placeholders:
                if placeholder in kwargs:
                    message = message.replace(f"{{{placeholder}}}", str(kwargs[placeholder]))
                else:
                    # Leave placeholder if value not provided
                    logger.warning(f"Placeholder '{placeholder}' not provided for template {template_id}")
            
            return message
        except Exception as e:
            logger.error(f"Error generating message from template {template_id}: {e}")
            return "Sorry, I encountered an error generating that message."
    
    def get_random_template(self, category: str) -> Optional[MessageTemplate]:
        """Get a random template from a specific category."""
        templates = self.get_templates_by_category(category)
        return random.choice(templates) if templates else None
    
    def generate_random_message(self, category: str, **kwargs) -> str:
        """Generate a random message from a category with provided parameters."""
        template = self.get_random_template(category)
        if not template:
            return f"No templates found for category '{category}'."
        
        return self.generate_message(template.template_id, **kwargs)
    
    def list_categories(self) -> List[str]:
        """Get list of all available categories."""
        return list(self.categories.keys())
    
    def get_template_stats(self) -> Dict[str, Any]:
        """Get statistics about template usage."""
        total_templates = len(self.templates)
        total_usage = sum(t.usage_count for t in self.templates.values())
        
        category_stats = {}
        for category, template_ids in self.categories.items():
            category_templates = [self.templates[tid] for tid in template_ids if tid in self.templates]
            category_stats[category] = {
                "count": len(category_templates),
                "total_usage": sum(t.usage_count for t in category_templates),
                "most_used": max(category_templates, key=lambda t: t.usage_count).template_id if category_templates else None
            }
        
        return {
            "total_templates": total_templates,
            "total_usage": total_usage,
            "categories": category_stats,
            "most_used_overall": max(self.templates.values(), key=lambda t: t.usage_count).template_id if self.templates else None
        }
    
    def export_templates(self, filename: str) -> None:
        """Export templates to a JSON file."""
        export_data = {
            "templates": [
                {
                    "template_id": t.template_id,
                    "category": t.category,
                    "content": t.content,
                    "placeholders": t.placeholders,
                    "usage_count": t.usage_count,
                    "created_at": t.created_at.isoformat()
                }
                for t in self.templates.values()
            ],
            "export_date": datetime.now().isoformat()
        }
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        logger.info(f"Exported {len(self.templates)} templates to {filename}")
    
    def import_templates(self, filename: str) -> int:
        """Import templates from a JSON file."""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            imported_count = 0
            for template_data in data.get("templates", []):
                template = MessageTemplate(
                    template_id=template_data["template_id"],
                    category=template_data["category"],
                    content=template_data["content"],
                    placeholders=template_data["placeholders"],
                    usage_count=template_data.get("usage_count", 0),
                    created_at=datetime.fromisoformat(template_data["created_at"])
                )
                self.add_template(template)
                imported_count += 1
            
            logger.info(f"Imported {imported_count} templates from {filename}")
            return imported_count
        
        except Exception as e:
            logger.error(f"Error importing templates from {filename}: {e}")
            return 0


# Global template manager instance
template_manager = TemplateManager()


def get_template_manager() -> TemplateManager:
    """Get the global template manager instance."""
    return template_manager


if __name__ == "__main__":
    # Demo the template system
    print("=== Fast Track Academy - Message Templates Demo ===")
    
    manager = get_template_manager()
    
    print(f"\nAvailable categories: {', '.join(manager.list_categories())}")
    
    # Demo different types of messages
    print("\n--- Greeting Messages ---")
    print(manager.generate_message("greeting_001", name="Alice", bot_name="DutyBot"))
    print(manager.generate_random_message("greeting", bot_name="DutyBot"))
    
    print("\n--- Course Messages ---")
    print(manager.generate_message("course_001", 
                                 course_name="Python Fundamentals",
                                 module_count="8",
                                 topics="variables, functions, and classes",
                                 progress="75"))
    
    print("\n--- Achievement Messages ---")
    print(manager.generate_message("achievement_001",
                                 name="Bob",
                                 achievement_name="Code Master",
                                 accomplishment="completing 50 coding exercises"))
    
    print("\n--- Social Media Messages ---")
    print(manager.generate_message("social_001",
                                 update_content="New interactive Python course now available! 🐍"))
    
    # Show statistics
    print("\n--- Template Statistics ---")
    stats = manager.get_template_stats()
    print(json.dumps(stats, indent=2))