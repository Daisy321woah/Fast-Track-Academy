"""
Fast Track Academy - Resources Management

This module manages learning resources, guides, documents, and external links
for the Fast Track Academy platform.
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
import os

logger = logging.getLogger(__name__)


class ResourceType(Enum):
    """Enumeration for resource types."""
    DOCUMENT = "document"
    VIDEO = "video"
    AUDIO = "audio"
    INTERACTIVE = "interactive"
    EXTERNAL_LINK = "external_link"
    GUIDE = "guide"
    TUTORIAL = "tutorial"
    REFERENCE = "reference"
    TEMPLATE = "template"


class AccessLevel(Enum):
    """Enumeration for resource access levels."""
    PUBLIC = "public"
    STUDENT = "student"
    PREMIUM = "premium"
    INSTRUCTOR = "instructor"
    ADMIN = "admin"


@dataclass
class Resource:
    """Data class representing a learning resource."""
    resource_id: str
    title: str
    description: str
    resource_type: ResourceType
    url: str
    access_level: AccessLevel = AccessLevel.PUBLIC
    tags: List[str] = field(default_factory=list)
    file_size: Optional[int] = None  # in bytes
    duration: Optional[int] = None  # in minutes for video/audio
    language: str = "en"
    difficulty_level: str = "beginner"
    author: str = "Fast Track Academy"
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    download_count: int = 0
    view_count: int = 0
    rating: float = 0.0
    rating_count: int = 0


@dataclass
class ResourceCollection:
    """Data class representing a collection of related resources."""
    collection_id: str
    name: str
    description: str
    resource_ids: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    access_level: AccessLevel = AccessLevel.PUBLIC
    created_at: datetime = field(default_factory=datetime.now)
    created_by: str = "system"


@dataclass
class UserResourceActivity:
    """Data class tracking user interactions with resources."""
    user_id: str
    resource_id: str
    activity_type: str  # viewed, downloaded, rated, bookmarked
    timestamp: datetime
    additional_data: Dict[str, Any] = field(default_factory=dict)


class ResourceManager:
    """Manages learning resources and collections."""
    
    def __init__(self):
        self.resources: Dict[str, Resource] = {}
        self.collections: Dict[str, ResourceCollection] = {}
        self.user_activities: List[UserResourceActivity] = []
        self.bookmarks: Dict[str, List[str]] = {}  # user_id -> list of resource_ids
        self._initialize_default_resources()
    
    def _initialize_default_resources(self) -> None:
        """Initialize the resource manager with default resources."""
        
        # Programming resources
        programming_resources = [
            Resource(
                resource_id="res_001",
                title="Python Programming Guide",
                description="Comprehensive guide to Python programming fundamentals",
                resource_type=ResourceType.DOCUMENT,
                url="/resources/docs/python-guide.pdf",
                tags=["python", "programming", "fundamentals"],
                file_size=2048000,  # 2MB
                difficulty_level="beginner",
                rating=4.7,
                rating_count=45
            ),
            Resource(
                resource_id="res_002",
                title="Python Setup Tutorial",
                description="Step-by-step video tutorial for setting up Python development environment",
                resource_type=ResourceType.VIDEO,
                url="/resources/videos/python-setup.mp4",
                tags=["python", "setup", "tutorial"],
                duration=15,
                difficulty_level="beginner",
                rating=4.9,
                rating_count=67
            ),
            Resource(
                resource_id="res_003",
                title="Python Cheat Sheet",
                description="Quick reference for Python syntax and common patterns",
                resource_type=ResourceType.REFERENCE,
                url="/resources/refs/python-cheatsheet.pdf",
                tags=["python", "reference", "syntax"],
                file_size=512000,  # 512KB
                difficulty_level="all",
                rating=4.8,
                rating_count=89
            )
        ]
        
        # Web development resources
        web_resources = [
            Resource(
                resource_id="res_004",
                title="HTML5 Interactive Tutorial",
                description="Interactive tutorial covering HTML5 features and best practices",
                resource_type=ResourceType.INTERACTIVE,
                url="/resources/interactive/html5-tutorial",
                tags=["html", "html5", "web development"],
                difficulty_level="beginner",
                rating=4.6,
                rating_count=34
            ),
            Resource(
                resource_id="res_005",
                title="CSS Grid Layout Guide",
                description="Complete guide to CSS Grid layout with examples",
                resource_type=ResourceType.GUIDE,
                url="/resources/guides/css-grid.html",
                tags=["css", "layout", "grid"],
                difficulty_level="intermediate",
                rating=4.8,
                rating_count=52
            ),
            Resource(
                resource_id="res_006",
                title="JavaScript Best Practices",
                description="Modern JavaScript best practices and coding standards",
                resource_type=ResourceType.DOCUMENT,
                url="/resources/docs/js-best-practices.md",
                tags=["javascript", "best practices", "coding standards"],
                difficulty_level="intermediate",
                rating=4.7,
                rating_count=78
            )
        ]
        
        # External resources
        external_resources = [
            Resource(
                resource_id="res_007",
                title="MDN Web Docs",
                description="Mozilla Developer Network - comprehensive web development documentation",
                resource_type=ResourceType.EXTERNAL_LINK,
                url="https://developer.mozilla.org/",
                tags=["documentation", "web development", "reference"],
                difficulty_level="all",
                rating=4.9,
                rating_count=156
            ),
            Resource(
                resource_id="res_008",
                title="Python.org Official Documentation",
                description="Official Python programming language documentation",
                resource_type=ResourceType.EXTERNAL_LINK,
                url="https://docs.python.org/",
                tags=["python", "documentation", "official"],
                difficulty_level="all",
                rating=4.8,
                rating_count=203
            )
        ]
        
        # Templates
        template_resources = [
            Resource(
                resource_id="res_009",
                title="Project Structure Template",
                description="Standard project structure template for Python projects",
                resource_type=ResourceType.TEMPLATE,
                url="/resources/templates/python-project-template.zip",
                tags=["python", "project", "template"],
                file_size=1024000,  # 1MB
                difficulty_level="beginner",
                rating=4.5,
                rating_count=23
            ),
            Resource(
                resource_id="res_010",
                title="HTML5 Website Template",
                description="Responsive HTML5 website template with modern design",
                resource_type=ResourceType.TEMPLATE,
                url="/resources/templates/html5-website-template.zip",
                tags=["html", "css", "template", "responsive"],
                file_size=3072000,  # 3MB
                difficulty_level="intermediate",
                rating=4.6,
                rating_count=41
            )
        ]
        
        # Add all resources
        all_resources = programming_resources + web_resources + external_resources + template_resources
        for resource in all_resources:
            self.add_resource(resource)
        
        # Create collections
        self._create_default_collections()
        
        logger.info(f"Initialized resource manager with {len(all_resources)} resources")
    
    def _create_default_collections(self) -> None:
        """Create default resource collections."""
        collections = [
            ResourceCollection(
                collection_id="col_001",
                name="Python Learning Path",
                description="Complete collection of Python learning resources",
                resource_ids=["res_001", "res_002", "res_003", "res_008", "res_009"],
                tags=["python", "learning path"]
            ),
            ResourceCollection(
                collection_id="col_002",
                name="Web Development Essentials",
                description="Essential resources for web development",
                resource_ids=["res_004", "res_005", "res_006", "res_007", "res_010"],
                tags=["web development", "essentials"]
            ),
            ResourceCollection(
                collection_id="col_003",
                name="Quick References",
                description="Quick reference materials and cheat sheets",
                resource_ids=["res_003", "res_007", "res_008"],
                tags=["reference", "quick access"]
            ),
            ResourceCollection(
                collection_id="col_004",
                name="Project Templates",
                description="Ready-to-use project templates",
                resource_ids=["res_009", "res_010"],
                tags=["templates", "projects"]
            )
        ]
        
        for collection in collections:
            self.add_collection(collection)
    
    def add_resource(self, resource: Resource) -> None:
        """Add a resource to the manager."""
        self.resources[resource.resource_id] = resource
        logger.info(f"Added resource: {resource.title}")
    
    def get_resource(self, resource_id: str) -> Optional[Resource]:
        """Get a resource by ID."""
        return self.resources.get(resource_id)
    
    def list_resources(self, 
                      resource_type: Optional[ResourceType] = None,
                      tags: Optional[List[str]] = None,
                      difficulty: Optional[str] = None,
                      access_level: Optional[AccessLevel] = None,
                      sort_by: str = "rating") -> List[Resource]:
        """List resources with optional filtering and sorting."""
        resources = list(self.resources.values())
        
        # Apply filters
        if resource_type:
            resources = [r for r in resources if r.resource_type == resource_type]
        
        if tags:
            resources = [r for r in resources if any(tag in r.tags for tag in tags)]
        
        if difficulty:
            resources = [r for r in resources if r.difficulty_level == difficulty or r.difficulty_level == "all"]
        
        if access_level:
            resources = [r for r in resources if r.access_level == access_level]
        
        # Sort resources
        if sort_by == "rating":
            resources.sort(key=lambda x: x.rating, reverse=True)
        elif sort_by == "views":
            resources.sort(key=lambda x: x.view_count, reverse=True)
        elif sort_by == "date":
            resources.sort(key=lambda x: x.created_at, reverse=True)
        elif sort_by == "title":
            resources.sort(key=lambda x: x.title)
        
        return resources
    
    def add_collection(self, collection: ResourceCollection) -> None:
        """Add a resource collection."""
        self.collections[collection.collection_id] = collection
        logger.info(f"Added collection: {collection.name}")
    
    def get_collection(self, collection_id: str) -> Optional[ResourceCollection]:
        """Get a collection by ID."""
        return self.collections.get(collection_id)
    
    def get_collection_resources(self, collection_id: str) -> List[Resource]:
        """Get all resources in a collection."""
        collection = self.get_collection(collection_id)
        if not collection:
            return []
        
        return [self.resources[rid] for rid in collection.resource_ids if rid in self.resources]
    
    def search_resources(self, query: str, 
                        resource_type: Optional[ResourceType] = None) -> List[Resource]:
        """Search resources by title, description, or tags."""
        query_lower = query.lower()
        results = []
        
        for resource in self.resources.values():
            if (query_lower in resource.title.lower() or
                query_lower in resource.description.lower() or
                any(query_lower in tag.lower() for tag in resource.tags)):
                
                if resource_type is None or resource.resource_type == resource_type:
                    results.append(resource)
        
        # Sort by relevance (title matches first, then description, then tags)
        def relevance_score(resource):
            score = 0
            if query_lower in resource.title.lower():
                score += 10
            if query_lower in resource.description.lower():
                score += 5
            score += sum(1 for tag in resource.tags if query_lower in tag.lower())
            return score
        
        results.sort(key=relevance_score, reverse=True)
        return results
    
    def record_activity(self, user_id: str, resource_id: str, 
                       activity_type: str, additional_data: Optional[Dict] = None) -> None:
        """Record user activity with a resource."""
        activity = UserResourceActivity(
            user_id=user_id,
            resource_id=resource_id,
            activity_type=activity_type,
            timestamp=datetime.now(),
            additional_data=additional_data or {}
        )
        
        self.user_activities.append(activity)
        
        # Update resource statistics
        resource = self.get_resource(resource_id)
        if resource:
            if activity_type == "viewed":
                resource.view_count += 1
            elif activity_type == "downloaded":
                resource.download_count += 1
        
        logger.info(f"Recorded {activity_type} activity for user {user_id} on resource {resource_id}")
    
    def rate_resource(self, user_id: str, resource_id: str, rating: float) -> bool:
        """Rate a resource (1-5 stars)."""
        if not (1 <= rating <= 5):
            return False
        
        resource = self.get_resource(resource_id)
        if not resource:
            return False
        
        # Simple rating calculation (in a real system, you'd track individual ratings)
        old_total = resource.rating * resource.rating_count
        resource.rating_count += 1
        resource.rating = (old_total + rating) / resource.rating_count
        
        self.record_activity(user_id, resource_id, "rated", {"rating": rating})
        
        logger.info(f"User {user_id} rated resource {resource_id}: {rating} stars")
        return True
    
    def bookmark_resource(self, user_id: str, resource_id: str) -> bool:
        """Bookmark a resource for a user."""
        if resource_id not in self.resources:
            return False
        
        if user_id not in self.bookmarks:
            self.bookmarks[user_id] = []
        
        if resource_id not in self.bookmarks[user_id]:
            self.bookmarks[user_id].append(resource_id)
            self.record_activity(user_id, resource_id, "bookmarked")
            return True
        
        return False  # Already bookmarked
    
    def get_user_bookmarks(self, user_id: str) -> List[Resource]:
        """Get all bookmarked resources for a user."""
        if user_id not in self.bookmarks:
            return []
        
        return [self.resources[rid] for rid in self.bookmarks[user_id] if rid in self.resources]
    
    def get_popular_resources(self, limit: int = 10) -> List[Resource]:
        """Get most popular resources based on views and ratings."""
        resources = list(self.resources.values())
        
        # Calculate popularity score (views + rating weight)
        def popularity_score(resource):
            return resource.view_count + (resource.rating * resource.rating_count * 10)
        
        resources.sort(key=popularity_score, reverse=True)
        return resources[:limit]
    
    def get_recent_resources(self, days: int = 30, limit: int = 10) -> List[Resource]:
        """Get recently added resources."""
        cutoff_date = datetime.now() - timedelta(days=days)
        recent = [r for r in self.resources.values() if r.created_at >= cutoff_date]
        recent.sort(key=lambda x: x.created_at, reverse=True)
        return recent[:limit]
    
    def get_user_recommendations(self, user_id: str, limit: int = 5) -> List[Resource]:
        """Get resource recommendations for a user based on their activity."""
        # Simple recommendation based on user's bookmarks and activity
        user_tags = set()
        
        # Get tags from bookmarked resources
        bookmarks = self.get_user_bookmarks(user_id)
        for resource in bookmarks:
            user_tags.update(resource.tags)
        
        # Get tags from viewed resources
        user_activities = [a for a in self.user_activities if a.user_id == user_id]
        for activity in user_activities:
            resource = self.get_resource(activity.resource_id)
            if resource:
                user_tags.update(resource.tags)
        
        if not user_tags:
            # Return popular resources if no activity history
            return self.get_popular_resources(limit)
        
        # Find resources with similar tags
        recommendations = []
        for resource in self.resources.values():
            if any(tag in user_tags for tag in resource.tags):
                # Don't recommend already bookmarked resources
                if user_id not in self.bookmarks or resource.resource_id not in self.bookmarks[user_id]:
                    recommendations.append(resource)
        
        # Sort by rating and return top recommendations
        recommendations.sort(key=lambda x: x.rating, reverse=True)
        return recommendations[:limit]
    
    def get_resource_stats(self) -> Dict[str, Any]:
        """Get comprehensive resource statistics."""
        total_resources = len(self.resources)
        total_collections = len(self.collections)
        total_activities = len(self.user_activities)
        
        # Resources by type
        type_counts = {}
        for resource in self.resources.values():
            type_name = resource.resource_type.value
            type_counts[type_name] = type_counts.get(type_name, 0) + 1
        
        # Most popular tags
        tag_counts = {}
        for resource in self.resources.values():
            for tag in resource.tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        popular_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            "total_resources": total_resources,
            "total_collections": total_collections,
            "total_user_activities": total_activities,
            "resources_by_type": type_counts,
            "popular_tags": dict(popular_tags),
            "average_rating": sum(r.rating for r in self.resources.values()) / total_resources if total_resources > 0 else 0,
            "total_views": sum(r.view_count for r in self.resources.values()),
            "total_downloads": sum(r.download_count for r in self.resources.values())
        }


# Global resource manager instance
resource_manager = ResourceManager()


def get_resource_manager() -> ResourceManager:
    """Get the global resource manager instance."""
    return resource_manager


if __name__ == "__main__":
    # Demo the resource management system
    print("=== Fast Track Academy - Resource Management Demo ===")
    
    manager = get_resource_manager()
    
    # List resources by category
    print("\nPython Resources:")
    python_resources = manager.list_resources(tags=["python"])
    for resource in python_resources[:3]:
        print(f"- {resource.title} ({resource.resource_type.value}) - Rating: {resource.rating}")
    
    print("\nWeb Development Resources:")
    web_resources = manager.list_resources(tags=["web development"])
    for resource in web_resources[:3]:
        print(f"- {resource.title} ({resource.resource_type.value}) - Rating: {resource.rating}")
    
    # Demo collections
    print(f"\nAvailable Collections: {len(manager.collections)}")
    for collection in manager.collections.values():
        resources_count = len(collection.resource_ids)
        print(f"- {collection.name}: {resources_count} resources")
    
    # Demo user interactions
    user_id = "student_001"
    print(f"\nUser Activity Demo for {user_id}:")
    
    # Bookmark some resources
    manager.bookmark_resource(user_id, "res_001")
    manager.bookmark_resource(user_id, "res_004")
    
    # Rate resources
    manager.rate_resource(user_id, "res_001", 5.0)
    manager.rate_resource(user_id, "res_002", 4.5)
    
    # Record some activity
    manager.record_activity(user_id, "res_001", "viewed")
    manager.record_activity(user_id, "res_002", "downloaded")
    
    # Get recommendations
    recommendations = manager.get_user_recommendations(user_id)
    print(f"Recommendations for {user_id}:")
    for rec in recommendations[:3]:
        print(f"- {rec.title} (Rating: {rec.rating})")
    
    # Search functionality
    print("\nSearch Results for 'python':")
    search_results = manager.search_resources("python")
    for result in search_results[:3]:
        print(f"- {result.title} ({result.resource_type.value})")
    
    # Statistics
    print("\nResource Statistics:")
    stats = manager.get_resource_stats()
    print(json.dumps(stats, indent=2))