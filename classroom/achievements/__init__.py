"""
Fast Track Academy - Achievements System

This module manages student achievements, badges, milestones, and progress tracking
to gamify the learning experience and motivate students.
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from enum import Enum
import math

logger = logging.getLogger(__name__)


class AchievementType(Enum):
    """Types of achievements available."""
    COURSE_COMPLETION = "course_completion"
    LESSON_STREAK = "lesson_streak"
    SKILL_MASTERY = "skill_mastery"
    TIME_SPENT = "time_spent"
    SOCIAL_ENGAGEMENT = "social_engagement"
    RESOURCE_USAGE = "resource_usage"
    MILESTONE = "milestone"
    SPECIAL_EVENT = "special_event"


class BadgeLevel(Enum):
    """Badge difficulty/rarity levels."""
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"
    DIAMOND = "diamond"


@dataclass
class Achievement:
    """Data class representing an achievement/badge."""
    achievement_id: str
    title: str
    description: str
    achievement_type: AchievementType
    badge_level: BadgeLevel
    icon_url: str
    requirements: Dict[str, Any]
    reward_points: int
    is_hidden: bool = False  # Hidden until unlocked
    unlock_message: str = ""
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class UserAchievement:
    """Data class representing a user's earned achievement."""
    user_id: str
    achievement_id: str
    earned_at: datetime
    progress_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class UserProgress:
    """Data class tracking user's overall progress and statistics."""
    user_id: str
    total_points: int = 0
    level: int = 1
    courses_completed: int = 0
    lessons_completed: int = 0
    time_spent_minutes: int = 0
    login_streak: int = 0
    last_login: Optional[datetime] = None
    achievements_earned: List[str] = field(default_factory=list)
    badges_by_level: Dict[str, int] = field(default_factory=lambda: {
        "bronze": 0, "silver": 0, "gold": 0, "platinum": 0, "diamond": 0
    })
    statistics: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


class AchievementSystem:
    """Main achievements system for managing badges, progress, and rewards."""
    
    def __init__(self):
        self.achievements: Dict[str, Achievement] = {}
        self.user_achievements: Dict[str, List[UserAchievement]] = {}
        self.user_progress: Dict[str, UserProgress] = {}
        self.leaderboard_cache: List[Dict] = []
        self._initialize_achievements()
    
    def _initialize_achievements(self) -> None:
        """Initialize the system with default achievements."""
        
        # Course completion achievements
        course_achievements = [
            Achievement(
                achievement_id="first_course",
                title="First Steps",
                description="Complete your first course",
                achievement_type=AchievementType.COURSE_COMPLETION,
                badge_level=BadgeLevel.BRONZE,
                icon_url="/icons/first-course.png",
                requirements={"courses_completed": 1},
                reward_points=100,
                unlock_message="Congratulations on completing your first course! You're on your way to mastering new skills!"
            ),
            Achievement(
                achievement_id="course_collector",
                title="Course Collector",
                description="Complete 5 courses",
                achievement_type=AchievementType.COURSE_COMPLETION,
                badge_level=BadgeLevel.SILVER,
                icon_url="/icons/course-collector.png",
                requirements={"courses_completed": 5},
                reward_points=500,
                unlock_message="Impressive! You've completed 5 courses. Your dedication to learning is remarkable!"
            ),
            Achievement(
                achievement_id="knowledge_master",
                title="Knowledge Master",
                description="Complete 10 courses",
                achievement_type=AchievementType.COURSE_COMPLETION,
                badge_level=BadgeLevel.GOLD,
                icon_url="/icons/knowledge-master.png",
                requirements={"courses_completed": 10},
                reward_points=1000,
                unlock_message="Outstanding! You're now a Knowledge Master with 10 completed courses!"
            )
        ]
        
        # Learning streak achievements
        streak_achievements = [
            Achievement(
                achievement_id="week_warrior",
                title="Week Warrior",
                description="Learn for 7 consecutive days",
                achievement_type=AchievementType.LESSON_STREAK,
                badge_level=BadgeLevel.BRONZE,
                icon_url="/icons/week-warrior.png",
                requirements={"login_streak": 7},
                reward_points=200,
                unlock_message="Amazing consistency! You've maintained a 7-day learning streak!"
            ),
            Achievement(
                achievement_id="month_champion",
                title="Month Champion",
                description="Learn for 30 consecutive days",
                achievement_type=AchievementType.LESSON_STREAK,
                badge_level=BadgeLevel.GOLD,
                icon_url="/icons/month-champion.png",
                requirements={"login_streak": 30},
                reward_points=1500,
                unlock_message="Incredible dedication! A full month of continuous learning!"
            )
        ]
        
        # Time-based achievements
        time_achievements = [
            Achievement(
                achievement_id="focused_learner",
                title="Focused Learner",
                description="Spend 10 hours learning",
                achievement_type=AchievementType.TIME_SPENT,
                badge_level=BadgeLevel.BRONZE,
                icon_url="/icons/focused-learner.png",
                requirements={"time_spent_minutes": 600},
                reward_points=300,
                unlock_message="Great focus! You've invested 10 hours in your learning journey!"
            ),
            Achievement(
                achievement_id="dedicated_student",
                title="Dedicated Student",
                description="Spend 50 hours learning",
                achievement_type=AchievementType.TIME_SPENT,
                badge_level=BadgeLevel.SILVER,
                icon_url="/icons/dedicated-student.png",
                requirements={"time_spent_minutes": 3000},
                reward_points=800,
                unlock_message="Remarkable dedication! 50 hours of focused learning!"
            ),
            Achievement(
                achievement_id="learning_enthusiast",
                title="Learning Enthusiast",
                description="Spend 100 hours learning",
                achievement_type=AchievementType.TIME_SPENT,
                badge_level=BadgeLevel.GOLD,
                icon_url="/icons/learning-enthusiast.png",
                requirements={"time_spent_minutes": 6000},
                reward_points=2000,
                unlock_message="Exceptional commitment! You're a true Learning Enthusiast!"
            )
        ]
        
        # Skill mastery achievements
        skill_achievements = [
            Achievement(
                achievement_id="python_novice",
                title="Python Novice",
                description="Complete Python fundamentals course",
                achievement_type=AchievementType.SKILL_MASTERY,
                badge_level=BadgeLevel.BRONZE,
                icon_url="/icons/python-novice.png",
                requirements={"course_completed": "course_python_001"},
                reward_points=250,
                unlock_message="Welcome to the world of Python! You've mastered the fundamentals!"
            ),
            Achievement(
                achievement_id="web_developer",
                title="Web Developer",
                description="Complete web development basics course",
                achievement_type=AchievementType.SKILL_MASTERY,
                badge_level=BadgeLevel.BRONZE,
                icon_url="/icons/web-developer.png",
                requirements={"course_completed": "course_web_001"},
                reward_points=250,
                unlock_message="Congratulations! You're now ready to build amazing websites!"
            )
        ]
        
        # Milestone achievements
        milestone_achievements = [
            Achievement(
                achievement_id="point_collector",
                title="Point Collector",
                description="Earn 1000 achievement points",
                achievement_type=AchievementType.MILESTONE,
                badge_level=BadgeLevel.SILVER,
                icon_url="/icons/point-collector.png",
                requirements={"total_points": 1000},
                reward_points=500,
                unlock_message="Excellent progress! You've collected 1000 achievement points!"
            ),
            Achievement(
                achievement_id="level_up_hero",
                title="Level Up Hero",
                description="Reach level 10",
                achievement_type=AchievementType.MILESTONE,
                badge_level=BadgeLevel.GOLD,
                icon_url="/icons/level-up-hero.png",
                requirements={"level": 10},
                reward_points=750,
                unlock_message="Level 10 achieved! You're becoming a learning legend!"
            )
        ]
        
        # Special achievements
        special_achievements = [
            Achievement(
                achievement_id="early_bird",
                title="Early Bird",
                description="Complete a lesson before 8 AM",
                achievement_type=AchievementType.SPECIAL_EVENT,
                badge_level=BadgeLevel.BRONZE,
                icon_url="/icons/early-bird.png",
                requirements={"early_morning_activity": True},
                reward_points=150,
                unlock_message="The early bird catches the worm! Great commitment to learning!"
            ),
            Achievement(
                achievement_id="night_owl",
                title="Night Owl",
                description="Complete a lesson after 10 PM",
                achievement_type=AchievementType.SPECIAL_EVENT,
                badge_level=BadgeLevel.BRONZE,
                icon_url="/icons/night-owl.png",
                requirements={"late_night_activity": True},
                reward_points=150,
                unlock_message="Burning the midnight oil! Your dedication knows no bounds!"
            )
        ]
        
        # Add all achievements
        all_achievements = (course_achievements + streak_achievements + 
                          time_achievements + skill_achievements + 
                          milestone_achievements + special_achievements)
        
        for achievement in all_achievements:
            self.add_achievement(achievement)
        
        logger.info(f"Initialized achievement system with {len(all_achievements)} achievements")
    
    def add_achievement(self, achievement: Achievement) -> None:
        """Add an achievement to the system."""
        self.achievements[achievement.achievement_id] = achievement
        logger.info(f"Added achievement: {achievement.title}")
    
    def get_achievement(self, achievement_id: str) -> Optional[Achievement]:
        """Get an achievement by ID."""
        return self.achievements.get(achievement_id)
    
    def get_user_progress(self, user_id: str) -> UserProgress:
        """Get or create user progress record."""
        if user_id not in self.user_progress:
            self.user_progress[user_id] = UserProgress(user_id=user_id)
        return self.user_progress[user_id]
    
    def update_user_activity(self, user_id: str, activity_data: Dict[str, Any]) -> List[str]:
        """Update user activity and check for new achievements."""
        progress = self.get_user_progress(user_id)
        progress.updated_at = datetime.now()
        
        # Update progress based on activity
        newly_earned = []
        
        if "course_completed" in activity_data:
            progress.courses_completed += 1
            newly_earned.extend(self._check_course_achievements(user_id, activity_data["course_completed"]))
        
        if "lesson_completed" in activity_data:
            progress.lessons_completed += 1
        
        if "time_spent" in activity_data:
            progress.time_spent_minutes += activity_data["time_spent"]
        
        if "login" in activity_data:
            self._update_login_streak(user_id)
        
        # Calculate level based on total points
        old_level = progress.level
        progress.level = self._calculate_level(progress.total_points)
        if progress.level > old_level:
            newly_earned.extend(self._check_level_achievements(user_id))
        
        # Check for time-based and milestone achievements
        newly_earned.extend(self._check_time_achievements(user_id))
        newly_earned.extend(self._check_milestone_achievements(user_id))
        newly_earned.extend(self._check_special_achievements(user_id, activity_data))
        
        return newly_earned
    
    def _calculate_level(self, total_points: int) -> int:
        """Calculate user level based on total points."""
        # Level formula: level = floor(sqrt(points / 100)) + 1
        return int(math.sqrt(total_points / 100)) + 1
    
    def _update_login_streak(self, user_id: str) -> None:
        """Update user's login streak."""
        progress = self.get_user_progress(user_id)
        now = datetime.now()
        
        if progress.last_login:
            days_since_last = (now - progress.last_login).days
            if days_since_last == 1:
                progress.login_streak += 1
            elif days_since_last > 1:
                progress.login_streak = 1
        else:
            progress.login_streak = 1
        
        progress.last_login = now
    
    def _check_course_achievements(self, user_id: str, course_id: str) -> List[str]:
        """Check for course-related achievements."""
        progress = self.get_user_progress(user_id)
        newly_earned = []
        
        # Check course completion count achievements
        for achievement in self.achievements.values():
            if (achievement.achievement_type == AchievementType.COURSE_COMPLETION and
                achievement.achievement_id not in progress.achievements_earned):
                
                if progress.courses_completed >= achievement.requirements.get("courses_completed", 0):
                    self._award_achievement(user_id, achievement.achievement_id)
                    newly_earned.append(achievement.achievement_id)
        
        # Check specific course achievements
        for achievement in self.achievements.values():
            if (achievement.achievement_type == AchievementType.SKILL_MASTERY and
                achievement.achievement_id not in progress.achievements_earned):
                
                required_course = achievement.requirements.get("course_completed")
                if required_course == course_id:
                    self._award_achievement(user_id, achievement.achievement_id)
                    newly_earned.append(achievement.achievement_id)
        
        return newly_earned
    
    def _check_time_achievements(self, user_id: str) -> List[str]:
        """Check for time-based achievements."""
        progress = self.get_user_progress(user_id)
        newly_earned = []
        
        for achievement in self.achievements.values():
            if (achievement.achievement_type == AchievementType.TIME_SPENT and
                achievement.achievement_id not in progress.achievements_earned):
                
                required_time = achievement.requirements.get("time_spent_minutes", 0)
                if progress.time_spent_minutes >= required_time:
                    self._award_achievement(user_id, achievement.achievement_id)
                    newly_earned.append(achievement.achievement_id)
            
            elif (achievement.achievement_type == AchievementType.LESSON_STREAK and
                  achievement.achievement_id not in progress.achievements_earned):
                
                required_streak = achievement.requirements.get("login_streak", 0)
                if progress.login_streak >= required_streak:
                    self._award_achievement(user_id, achievement.achievement_id)
                    newly_earned.append(achievement.achievement_id)
        
        return newly_earned
    
    def _check_milestone_achievements(self, user_id: str) -> List[str]:
        """Check for milestone achievements."""
        progress = self.get_user_progress(user_id)
        newly_earned = []
        
        for achievement in self.achievements.values():
            if (achievement.achievement_type == AchievementType.MILESTONE and
                achievement.achievement_id not in progress.achievements_earned):
                
                if ("total_points" in achievement.requirements and
                    progress.total_points >= achievement.requirements["total_points"]):
                    self._award_achievement(user_id, achievement.achievement_id)
                    newly_earned.append(achievement.achievement_id)
        
        return newly_earned
    
    def _check_level_achievements(self, user_id: str) -> List[str]:
        """Check for level-based achievements."""
        progress = self.get_user_progress(user_id)
        newly_earned = []
        
        for achievement in self.achievements.values():
            if (achievement.achievement_type == AchievementType.MILESTONE and
                achievement.achievement_id not in progress.achievements_earned):
                
                if ("level" in achievement.requirements and
                    progress.level >= achievement.requirements["level"]):
                    self._award_achievement(user_id, achievement.achievement_id)
                    newly_earned.append(achievement.achievement_id)
        
        return newly_earned
    
    def _check_special_achievements(self, user_id: str, activity_data: Dict[str, Any]) -> List[str]:
        """Check for special event achievements."""
        progress = self.get_user_progress(user_id)
        newly_earned = []
        current_time = datetime.now()
        
        for achievement in self.achievements.values():
            if (achievement.achievement_type == AchievementType.SPECIAL_EVENT and
                achievement.achievement_id not in progress.achievements_earned):
                
                # Early bird achievement (before 8 AM)
                if (achievement.achievement_id == "early_bird" and
                    current_time.hour < 8):
                    self._award_achievement(user_id, achievement.achievement_id)
                    newly_earned.append(achievement.achievement_id)
                
                # Night owl achievement (after 10 PM)
                elif (achievement.achievement_id == "night_owl" and
                      current_time.hour >= 22):
                    self._award_achievement(user_id, achievement.achievement_id)
                    newly_earned.append(achievement.achievement_id)
        
        return newly_earned
    
    def _award_achievement(self, user_id: str, achievement_id: str) -> None:
        """Award an achievement to a user."""
        achievement = self.get_achievement(achievement_id)
        if not achievement:
            return
        
        progress = self.get_user_progress(user_id)
        progress.achievements_earned.append(achievement_id)
        progress.total_points += achievement.reward_points
        
        # Update badge count
        badge_level = achievement.badge_level.value
        progress.badges_by_level[badge_level] += 1
        
        # Record the achievement
        if user_id not in self.user_achievements:
            self.user_achievements[user_id] = []
        
        user_achievement = UserAchievement(
            user_id=user_id,
            achievement_id=achievement_id,
            earned_at=datetime.now()
        )
        
        self.user_achievements[user_id].append(user_achievement)
        
        logger.info(f"Awarded achievement '{achievement.title}' to user {user_id}")
    
    def get_user_achievements(self, user_id: str) -> List[UserAchievement]:
        """Get all achievements earned by a user."""
        return self.user_achievements.get(user_id, [])
    
    def get_user_badges_summary(self, user_id: str) -> Dict[str, Any]:
        """Get a summary of user's badges and achievements."""
        progress = self.get_user_progress(user_id)
        achievements = self.get_user_achievements(user_id)
        
        recent_achievements = sorted(achievements, key=lambda x: x.earned_at, reverse=True)[:5]
        
        return {
            "user_id": user_id,
            "level": progress.level,
            "total_points": progress.total_points,
            "total_achievements": len(achievements),
            "badges_by_level": progress.badges_by_level,
            "recent_achievements": [
                {
                    "achievement_id": ua.achievement_id,
                    "title": self.get_achievement(ua.achievement_id).title,
                    "earned_at": ua.earned_at.isoformat()
                }
                for ua in recent_achievements
            ],
            "progress_stats": {
                "courses_completed": progress.courses_completed,
                "lessons_completed": progress.lessons_completed,
                "time_spent_hours": round(progress.time_spent_minutes / 60, 1),
                "login_streak": progress.login_streak
            }
        }
    
    def get_leaderboard(self, category: str = "points", limit: int = 10) -> List[Dict[str, Any]]:
        """Get leaderboard rankings."""
        users = list(self.user_progress.values())
        
        if category == "points":
            users.sort(key=lambda x: x.total_points, reverse=True)
        elif category == "level":
            users.sort(key=lambda x: x.level, reverse=True)
        elif category == "courses":
            users.sort(key=lambda x: x.courses_completed, reverse=True)
        elif category == "time":
            users.sort(key=lambda x: x.time_spent_minutes, reverse=True)
        
        leaderboard = []
        for i, user in enumerate(users[:limit]):
            leaderboard.append({
                "rank": i + 1,
                "user_id": user.user_id,
                "level": user.level,
                "total_points": user.total_points,
                "achievements_count": len(user.achievements_earned),
                "courses_completed": user.courses_completed,
                "time_spent_hours": round(user.time_spent_minutes / 60, 1)
            })
        
        return leaderboard
    
    def get_achievement_progress(self, user_id: str) -> Dict[str, Any]:
        """Get user's progress towards unearned achievements."""
        progress = self.get_user_progress(user_id)
        achievement_progress = {}
        
        for achievement in self.achievements.values():
            if achievement.achievement_id not in progress.achievements_earned:
                progress_info = {
                    "achievement_id": achievement.achievement_id,
                    "title": achievement.title,
                    "description": achievement.description,
                    "badge_level": achievement.badge_level.value,
                    "reward_points": achievement.reward_points,
                    "progress_percentage": 0
                }
                
                # Calculate progress percentage based on requirements
                if "courses_completed" in achievement.requirements:
                    required = achievement.requirements["courses_completed"]
                    current = progress.courses_completed
                    progress_info["progress_percentage"] = min(100, (current / required) * 100)
                
                elif "time_spent_minutes" in achievement.requirements:
                    required = achievement.requirements["time_spent_minutes"]
                    current = progress.time_spent_minutes
                    progress_info["progress_percentage"] = min(100, (current / required) * 100)
                
                elif "login_streak" in achievement.requirements:
                    required = achievement.requirements["login_streak"]
                    current = progress.login_streak
                    progress_info["progress_percentage"] = min(100, (current / required) * 100)
                
                elif "total_points" in achievement.requirements:
                    required = achievement.requirements["total_points"]
                    current = progress.total_points
                    progress_info["progress_percentage"] = min(100, (current / required) * 100)
                
                elif "level" in achievement.requirements:
                    required = achievement.requirements["level"]
                    current = progress.level
                    progress_info["progress_percentage"] = min(100, (current / required) * 100)
                
                achievement_progress[achievement.achievement_id] = progress_info
        
        return achievement_progress
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get comprehensive achievement system statistics."""
        total_users = len(self.user_progress)
        total_achievements = len(self.achievements)
        total_earned_achievements = sum(len(ua) for ua in self.user_achievements.values())
        
        # Achievements by type
        achievements_by_type = {}
        for achievement in self.achievements.values():
            type_name = achievement.achievement_type.value
            achievements_by_type[type_name] = achievements_by_type.get(type_name, 0) + 1
        
        # Most earned achievements
        achievement_counts = {}
        for user_achievements in self.user_achievements.values():
            for ua in user_achievements:
                achievement_counts[ua.achievement_id] = achievement_counts.get(ua.achievement_id, 0) + 1
        
        most_earned = sorted(achievement_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "total_users": total_users,
            "total_achievements": total_achievements,
            "total_earned_achievements": total_earned_achievements,
            "achievements_by_type": achievements_by_type,
            "most_earned_achievements": [
                {
                    "achievement_id": aid,
                    "title": self.get_achievement(aid).title,
                    "earned_count": count
                }
                for aid, count in most_earned
            ],
            "average_achievements_per_user": total_earned_achievements / total_users if total_users > 0 else 0
        }


# Global achievement system instance
achievement_system = AchievementSystem()


def get_achievement_system() -> AchievementSystem:
    """Get the global achievement system instance."""
    return achievement_system


if __name__ == "__main__":
    # Demo the achievement system
    print("=== Fast Track Academy - Achievement System Demo ===")
    
    system = get_achievement_system()
    
    # Simulate user activity
    user_id = "student_001"
    print(f"\nSimulating activity for {user_id}...")
    
    # User completes some courses and lessons
    newly_earned = system.update_user_activity(user_id, {
        "course_completed": "course_python_001",
        "lesson_completed": True,
        "time_spent": 45,
        "login": True
    })
    
    if newly_earned:
        print(f"New achievements earned: {newly_earned}")
    
    # Simulate more activity over time
    for day in range(8):
        newly_earned = system.update_user_activity(user_id, {
            "lesson_completed": True,
            "time_spent": 30,
            "login": True
        })
        if newly_earned:
            print(f"Day {day + 1} - New achievements: {newly_earned}")
    
    # Complete another course
    newly_earned = system.update_user_activity(user_id, {
        "course_completed": "course_web_001",
        "time_spent": 60
    })
    
    if newly_earned:
        print(f"New achievements after second course: {newly_earned}")
    
    # Get user summary
    print(f"\nUser Badge Summary for {user_id}:")
    summary = system.get_user_badges_summary(user_id)
    print(json.dumps(summary, indent=2, default=str))
    
    # Show achievement progress
    print(f"\nAchievement Progress for {user_id}:")
    progress = system.get_achievement_progress(user_id)
    for achievement_id, info in list(progress.items())[:3]:
        print(f"- {info['title']}: {info['progress_percentage']:.1f}% complete")
    
    # Show leaderboard
    print("\nLeaderboard (Top 3):")
    leaderboard = system.get_leaderboard(limit=3)
    for entry in leaderboard:
        print(f"{entry['rank']}. User {entry['user_id']} - Level {entry['level']} ({entry['total_points']} points)")
    
    # System statistics
    print("\nSystem Statistics:")
    stats = system.get_system_stats()
    print(json.dumps(stats, indent=2))