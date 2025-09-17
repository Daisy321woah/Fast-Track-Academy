"""
Fast Track Academy - Classroom Dashboard

This module provides the core dashboard functionality for navigating
lessons, guides, and resources in the Fast Track Academy platform.
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class LessonStatus(Enum):
    """Enumeration for lesson completion status."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    LOCKED = "locked"


class DifficultyLevel(Enum):
    """Enumeration for content difficulty levels."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


@dataclass
class Lesson:
    """Data class representing a lesson."""
    lesson_id: str
    title: str
    description: str
    content_url: str
    difficulty: DifficultyLevel
    estimated_duration: int  # in minutes
    prerequisites: List[str] = field(default_factory=list)
    status: LessonStatus = LessonStatus.NOT_STARTED
    progress_percentage: float = 0.0
    completed_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Course:
    """Data class representing a course."""
    course_id: str
    title: str
    description: str
    instructor: str
    lessons: List[Lesson] = field(default_factory=list)
    total_duration: int = 0  # in minutes
    difficulty: DifficultyLevel = DifficultyLevel.BEGINNER
    tags: List[str] = field(default_factory=list)
    enrollment_count: int = 0
    rating: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class StudentProgress:
    """Data class representing a student's progress."""
    student_id: str
    course_id: str
    enrolled_at: datetime
    last_accessed: datetime
    completed_lessons: List[str] = field(default_factory=list)
    current_lesson: Optional[str] = None
    overall_progress: float = 0.0
    total_time_spent: int = 0  # in minutes


class Dashboard:
    """Main dashboard class for managing courses and student progress."""
    
    def __init__(self):
        self.courses: Dict[str, Course] = {}
        self.student_progress: Dict[str, List[StudentProgress]] = {}
        self.resources: Dict[str, Any] = {}
        self._initialize_sample_data()
    
    def _initialize_sample_data(self) -> None:
        """Initialize the dashboard with sample courses and lessons."""
        
        # Python Fundamentals Course
        python_lessons = [
            Lesson(
                lesson_id="py_001",
                title="Introduction to Python",
                description="Learn the basics of Python programming language",
                content_url="/content/python/intro",
                difficulty=DifficultyLevel.BEGINNER,
                estimated_duration=30
            ),
            Lesson(
                lesson_id="py_002",
                title="Variables and Data Types",
                description="Understanding Python variables and basic data types",
                content_url="/content/python/variables",
                difficulty=DifficultyLevel.BEGINNER,
                estimated_duration=45,
                prerequisites=["py_001"]
            ),
            Lesson(
                lesson_id="py_003",
                title="Control Structures",
                description="If statements, loops, and conditional logic",
                content_url="/content/python/control",
                difficulty=DifficultyLevel.BEGINNER,
                estimated_duration=60,
                prerequisites=["py_002"]
            ),
            Lesson(
                lesson_id="py_004",
                title="Functions and Modules",
                description="Creating and using functions, importing modules",
                content_url="/content/python/functions",
                difficulty=DifficultyLevel.INTERMEDIATE,
                estimated_duration=75,
                prerequisites=["py_003"]
            )
        ]
        
        python_course = Course(
            course_id="course_python_001",
            title="Python Fundamentals",
            description="Complete introduction to Python programming for beginners",
            instructor="Dr. Sarah Chen",
            lessons=python_lessons,
            total_duration=sum(lesson.estimated_duration for lesson in python_lessons),
            difficulty=DifficultyLevel.BEGINNER,
            tags=["programming", "python", "beginner", "fundamentals"],
            enrollment_count=150,
            rating=4.8
        )
        
        # Web Development Course
        web_lessons = [
            Lesson(
                lesson_id="web_001",
                title="HTML Basics",
                description="Introduction to HTML structure and elements",
                content_url="/content/web/html",
                difficulty=DifficultyLevel.BEGINNER,
                estimated_duration=40
            ),
            Lesson(
                lesson_id="web_002",
                title="CSS Styling",
                description="Styling web pages with CSS",
                content_url="/content/web/css",
                difficulty=DifficultyLevel.BEGINNER,
                estimated_duration=50,
                prerequisites=["web_001"]
            ),
            Lesson(
                lesson_id="web_003",
                title="JavaScript Fundamentals",
                description="Adding interactivity with JavaScript",
                content_url="/content/web/javascript",
                difficulty=DifficultyLevel.INTERMEDIATE,
                estimated_duration=80,
                prerequisites=["web_002"]
            )
        ]
        
        web_course = Course(
            course_id="course_web_001",
            title="Web Development Basics",
            description="Learn to build modern websites from scratch",
            instructor="Prof. Mike Johnson",
            lessons=web_lessons,
            total_duration=sum(lesson.estimated_duration for lesson in web_lessons),
            difficulty=DifficultyLevel.BEGINNER,
            tags=["web development", "html", "css", "javascript"],
            enrollment_count=200,
            rating=4.6
        )
        
        self.add_course(python_course)
        self.add_course(web_course)
        
        # Add sample resources
        self.resources = {
            "programming_guides": [
                {
                    "title": "Python Style Guide",
                    "url": "/resources/python-style-guide",
                    "type": "document",
                    "difficulty": "intermediate"
                },
                {
                    "title": "Debugging Best Practices",
                    "url": "/resources/debugging-guide",
                    "type": "guide",
                    "difficulty": "beginner"
                }
            ],
            "video_tutorials": [
                {
                    "title": "Setting up Development Environment",
                    "url": "/resources/videos/dev-setup",
                    "duration": "15 min",
                    "type": "video"
                }
            ],
            "external_links": [
                {
                    "title": "Python Official Documentation",
                    "url": "https://docs.python.org/",
                    "type": "documentation"
                }
            ]
        }
        
        logger.info("Dashboard initialized with sample data")
    
    def add_course(self, course: Course) -> None:
        """Add a course to the dashboard."""
        self.courses[course.course_id] = course
        logger.info(f"Added course: {course.title}")
    
    def get_course(self, course_id: str) -> Optional[Course]:
        """Get a course by ID."""
        return self.courses.get(course_id)
    
    def list_courses(self, difficulty: Optional[DifficultyLevel] = None, 
                    tags: Optional[List[str]] = None) -> List[Course]:
        """List courses with optional filtering."""
        courses = list(self.courses.values())
        
        if difficulty:
            courses = [c for c in courses if c.difficulty == difficulty]
        
        if tags:
            courses = [c for c in courses if any(tag in c.tags for tag in tags)]
        
        return sorted(courses, key=lambda x: x.rating, reverse=True)
    
    def enroll_student(self, student_id: str, course_id: str) -> bool:
        """Enroll a student in a course."""
        course = self.get_course(course_id)
        if not course:
            logger.error(f"Course {course_id} not found")
            return False
        
        if student_id not in self.student_progress:
            self.student_progress[student_id] = []
        
        # Check if already enrolled
        for progress in self.student_progress[student_id]:
            if progress.course_id == course_id:
                logger.warning(f"Student {student_id} already enrolled in {course_id}")
                return False
        
        progress = StudentProgress(
            student_id=student_id,
            course_id=course_id,
            enrolled_at=datetime.now(),
            last_accessed=datetime.now()
        )
        
        self.student_progress[student_id].append(progress)
        course.enrollment_count += 1
        
        logger.info(f"Enrolled student {student_id} in course {course_id}")
        return True
    
    def get_student_progress(self, student_id: str, course_id: Optional[str] = None) -> List[StudentProgress]:
        """Get student progress for specific course or all courses."""
        if student_id not in self.student_progress:
            return []
        
        progress_list = self.student_progress[student_id]
        
        if course_id:
            return [p for p in progress_list if p.course_id == course_id]
        
        return progress_list
    
    def update_lesson_progress(self, student_id: str, course_id: str, 
                             lesson_id: str, progress_percentage: float) -> bool:
        """Update a student's progress on a specific lesson."""
        student_progress = self.get_student_progress(student_id, course_id)
        if not student_progress:
            logger.error(f"Student {student_id} not enrolled in course {course_id}")
            return False
        
        progress = student_progress[0]
        progress.last_accessed = datetime.now()
        progress.current_lesson = lesson_id
        
        # Update lesson status in course
        course = self.get_course(course_id)
        if course:
            for lesson in course.lessons:
                if lesson.lesson_id == lesson_id:
                    lesson.progress_percentage = progress_percentage
                    if progress_percentage >= 100:
                        lesson.status = LessonStatus.COMPLETED
                        lesson.completed_at = datetime.now()
                        if lesson_id not in progress.completed_lessons:
                            progress.completed_lessons.append(lesson_id)
                    elif progress_percentage > 0:
                        lesson.status = LessonStatus.IN_PROGRESS
                    break
        
        # Calculate overall course progress
        progress.overall_progress = self._calculate_course_progress(student_id, course_id)
        
        logger.info(f"Updated progress for student {student_id}, lesson {lesson_id}: {progress_percentage}%")
        return True
    
    def _calculate_course_progress(self, student_id: str, course_id: str) -> float:
        """Calculate overall course progress for a student."""
        course = self.get_course(course_id)
        if not course or not course.lessons:
            return 0.0
        
        total_progress = sum(lesson.progress_percentage for lesson in course.lessons)
        return total_progress / len(course.lessons)
    
    def get_dashboard_summary(self, student_id: str) -> Dict[str, Any]:
        """Get a summary dashboard for a student."""
        student_courses = self.get_student_progress(student_id)
        
        summary = {
            "student_id": student_id,
            "enrolled_courses": len(student_courses),
            "total_courses_available": len(self.courses),
            "courses": [],
            "recent_activity": [],
            "recommendations": []
        }
        
        for progress in student_courses:
            course = self.get_course(progress.course_id)
            if course:
                course_summary = {
                    "course_id": course.course_id,
                    "title": course.title,
                    "instructor": course.instructor,
                    "progress": progress.overall_progress,
                    "completed_lessons": len(progress.completed_lessons),
                    "total_lessons": len(course.lessons),
                    "current_lesson": progress.current_lesson,
                    "last_accessed": progress.last_accessed.isoformat()
                }
                summary["courses"].append(course_summary)
        
        # Get recent activity (last 7 days)
        week_ago = datetime.now() - timedelta(days=7)
        recent_progress = [p for p in student_courses if p.last_accessed >= week_ago]
        summary["recent_activity"] = [
            {
                "course_title": self.get_course(p.course_id).title,
                "last_accessed": p.last_accessed.isoformat()
            }
            for p in recent_progress
        ]
        
        # Simple recommendations based on tags
        enrolled_course_ids = [p.course_id for p in student_courses]
        available_courses = [c for c in self.courses.values() if c.course_id not in enrolled_course_ids]
        summary["recommendations"] = [
            {
                "course_id": course.course_id,
                "title": course.title,
                "rating": course.rating,
                "difficulty": course.difficulty.value
            }
            for course in available_courses[:3]  # Top 3 recommendations
        ]
        
        return summary
    
    def get_resources(self, category: Optional[str] = None) -> Dict[str, Any]:
        """Get learning resources, optionally filtered by category."""
        if category and category in self.resources:
            return {category: self.resources[category]}
        return self.resources
    
    def search_content(self, query: str) -> Dict[str, List[Dict]]:
        """Search for courses and resources by query."""
        results = {
            "courses": [],
            "lessons": [],
            "resources": []
        }
        
        query_lower = query.lower()
        
        # Search courses
        for course in self.courses.values():
            if (query_lower in course.title.lower() or 
                query_lower in course.description.lower() or
                any(query_lower in tag for tag in course.tags)):
                results["courses"].append({
                    "type": "course",
                    "id": course.course_id,
                    "title": course.title,
                    "description": course.description,
                    "rating": course.rating
                })
        
        # Search lessons
        for course in self.courses.values():
            for lesson in course.lessons:
                if (query_lower in lesson.title.lower() or 
                    query_lower in lesson.description.lower()):
                    results["lessons"].append({
                        "type": "lesson",
                        "id": lesson.lesson_id,
                        "title": lesson.title,
                        "course_title": course.title,
                        "description": lesson.description
                    })
        
        return results


# Global dashboard instance
dashboard = Dashboard()


def get_dashboard() -> Dashboard:
    """Get the global dashboard instance."""
    return dashboard


if __name__ == "__main__":
    # Demo the dashboard functionality
    print("=== Fast Track Academy - Classroom Dashboard Demo ===")
    
    dash = get_dashboard()
    
    # List available courses
    print("\nAvailable Courses:")
    courses = dash.list_courses()
    for course in courses:
        print(f"- {course.title} ({course.difficulty.value}) - Rating: {course.rating}")
    
    # Enroll a student
    student_id = "student_001"
    print(f"\nEnrolling student {student_id}...")
    dash.enroll_student(student_id, "course_python_001")
    dash.enroll_student(student_id, "course_web_001")
    
    # Update some progress
    print("\nUpdating lesson progress...")
    dash.update_lesson_progress(student_id, "course_python_001", "py_001", 100)
    dash.update_lesson_progress(student_id, "course_python_001", "py_002", 50)
    
    # Get dashboard summary
    print("\nDashboard Summary:")
    summary = dash.get_dashboard_summary(student_id)
    print(json.dumps(summary, indent=2, default=str))
    
    # Search functionality
    print("\nSearch Results for 'python':")
    search_results = dash.search_content("python")
    print(json.dumps(search_results, indent=2))