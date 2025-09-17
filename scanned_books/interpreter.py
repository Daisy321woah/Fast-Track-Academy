"""
Fast Track Academy - Scanned Books Interpreter

This module provides functionality for processing, analyzing, and interpreting
scanned book content for integration into the academy platform.
"""

import os
import re
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from collections import Counter
import math

logger = logging.getLogger(__name__)


@dataclass
class BookSection:
    """Data class representing a section of a book."""
    section_id: str
    title: str
    content: str
    level: int  # Header level (1, 2, 3, etc.)
    word_count: int
    start_line: int
    end_line: int
    parent_section: Optional[str] = None
    subsections: List[str] = field(default_factory=list)


@dataclass
class BookMetadata:
    """Data class containing book metadata."""
    book_id: str
    title: str
    filename: str
    total_words: int
    total_lines: int
    sections_count: int
    chapters_count: int
    reading_time_minutes: int
    topics: List[str] = field(default_factory=list)
    difficulty_level: str = "intermediate"
    processed_at: datetime = field(default_factory=datetime.now)


@dataclass
class SearchResult:
    """Data class for search results."""
    book_id: str
    section_id: str
    section_title: str
    content_snippet: str
    relevance_score: float
    match_positions: List[Tuple[int, int]] = field(default_factory=list)


class BookInterpreter:
    """Main class for interpreting and processing scanned book content."""
    
    def __init__(self, books_directory: str = "/home/runner/work/Fast-Track-Academy/Fast-Track-Academy/scanned_books"):
        self.books_directory = books_directory
        self.books: Dict[str, BookMetadata] = {}
        self.sections: Dict[str, Dict[str, BookSection]] = {}
        self.word_index: Dict[str, List[Tuple[str, str]]] = {}  # word -> [(book_id, section_id)]
        self._load_books()
    
    def _load_books(self) -> None:
        """Load and process all books in the directory."""
        if not os.path.exists(self.books_directory):
            logger.warning(f"Books directory {self.books_directory} does not exist")
            return
        
        for filename in os.listdir(self.books_directory):
            if filename.endswith('.txt'):
                filepath = os.path.join(self.books_directory, filename)
                self._process_book(filepath)
        
        self._build_word_index()
        logger.info(f"Loaded and processed {len(self.books)} books")
    
    def _process_book(self, filepath: str) -> None:
        """Process a single book file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
            
            filename = os.path.basename(filepath)
            book_id = filename.replace('.txt', '')
            
            # Extract sections
            sections = self._extract_sections(content)
            
            # Calculate metadata
            total_words = len(content.split())
            total_lines = len(content.split('\n'))
            reading_time = math.ceil(total_words / 200)  # Assuming 200 words per minute
            
            # Extract title from first header or filename
            title = self._extract_title(content, filename)
            
            # Identify topics
            topics = self._extract_topics(content)
            
            # Determine difficulty level
            difficulty = self._assess_difficulty(content)
            
            metadata = BookMetadata(
                book_id=book_id,
                title=title,
                filename=filename,
                total_words=total_words,
                total_lines=total_lines,
                sections_count=len(sections),
                chapters_count=len([s for s in sections.values() if s.level == 1]),
                reading_time_minutes=reading_time,
                topics=topics,
                difficulty_level=difficulty
            )
            
            self.books[book_id] = metadata
            self.sections[book_id] = sections
            
            logger.info(f"Processed book: {title} ({len(sections)} sections)")
            
        except Exception as e:
            logger.error(f"Error processing book {filepath}: {e}")
    
    def _extract_sections(self, content: str) -> Dict[str, BookSection]:
        """Extract sections from book content based on headers."""
        sections = {}
        lines = content.split('\n')
        current_section = None
        section_content = []
        section_counter = 0
        
        for line_num, line in enumerate(lines):
            stripped_line = line.strip()
            
            # Check if line is a header (starts with # or is all caps)
            header_level = self._get_header_level(stripped_line)
            
            if header_level > 0 or self._is_chapter_header(stripped_line):
                # Save previous section
                if current_section:
                    content_text = '\n'.join(section_content).strip()
                    if content_text:  # Only save non-empty sections
                        current_section.content = content_text
                        current_section.word_count = len(content_text.split())
                        current_section.end_line = line_num - 1
                        sections[current_section.section_id] = current_section
                
                # Start new section
                section_counter += 1
                section_id = f"section_{section_counter:03d}"
                title = self._clean_header(stripped_line)
                
                current_section = BookSection(
                    section_id=section_id,
                    title=title,
                    content="",
                    level=header_level if header_level > 0 else 1,
                    word_count=0,
                    start_line=line_num,
                    end_line=line_num
                )
                
                section_content = []
            else:
                # Add line to current section content
                if stripped_line:  # Skip empty lines
                    section_content.append(line)
        
        # Save final section
        if current_section and section_content:
            content_text = '\n'.join(section_content).strip()
            current_section.content = content_text
            current_section.word_count = len(content_text.split())
            current_section.end_line = len(lines) - 1
            sections[current_section.section_id] = current_section
        
        # Establish parent-child relationships
        self._establish_section_hierarchy(sections)
        
        return sections
    
    def _get_header_level(self, line: str) -> int:
        """Determine header level based on markdown-style headers."""
        if line.startswith('#'):
            return len(line) - len(line.lstrip('#'))
        return 0
    
    def _is_chapter_header(self, line: str) -> bool:
        """Check if line looks like a chapter header."""
        patterns = [
            r'^Chapter \d+',
            r'^CHAPTER \d+',
            r'^Part \d+',
            r'^Section \d+',
        ]
        
        for pattern in patterns:
            if re.match(pattern, line, re.IGNORECASE):
                return True
        
        # Check if line is short and mostly uppercase
        if len(line) < 50 and line.isupper() and len(line.split()) < 8:
            return True
        
        return False
    
    def _clean_header(self, header: str) -> str:
        """Clean and format header text."""
        # Remove markdown symbols
        header = re.sub(r'^#+\s*', '', header)
        
        # Remove common prefixes
        header = re.sub(r'^(Chapter|CHAPTER|Part|Section)\s*\d+:?\s*', '', header, flags=re.IGNORECASE)
        
        return header.strip()
    
    def _establish_section_hierarchy(self, sections: Dict[str, BookSection]) -> None:
        """Establish parent-child relationships between sections."""
        section_list = list(sections.values())
        
        for i, section in enumerate(section_list):
            # Find parent section (previous section with lower level)
            for j in range(i - 1, -1, -1):
                parent_candidate = section_list[j]
                if parent_candidate.level < section.level:
                    section.parent_section = parent_candidate.section_id
                    parent_candidate.subsections.append(section.section_id)
                    break
    
    def _extract_title(self, content: str, filename: str) -> str:
        """Extract book title from content or filename."""
        lines = content.split('\n')
        
        # Look for first header
        for line in lines[:10]:  # Check first 10 lines
            stripped = line.strip()
            if stripped.startswith('#'):
                return self._clean_header(stripped)
            elif self._is_chapter_header(stripped) and 'chapter' not in stripped.lower():
                return stripped
        
        # Fallback to filename
        return filename.replace('.txt', '').replace('_', ' ').replace('-', ' ').title()
    
    def _extract_topics(self, content: str) -> List[str]:
        """Extract topics/keywords from content."""
        # Common programming and learning keywords
        topic_keywords = {
            'programming': ['python', 'javascript', 'code', 'programming', 'algorithm', 'function', 'class', 'object'],
            'web development': ['html', 'css', 'web', 'website', 'frontend', 'backend', 'api'],
            'learning': ['learning', 'study', 'education', 'knowledge', 'skill', 'practice'],
            'memory': ['memory', 'retention', 'recall', 'memorization', 'mnemonics'],
            'database': ['database', 'sql', 'query', 'table', 'index', 'normalization'],
            'testing': ['test', 'testing', 'unit test', 'integration', 'quality'],
            'design patterns': ['pattern', 'singleton', 'factory', 'observer', 'strategy'],
            'data structures': ['array', 'list', 'tree', 'graph', 'stack', 'queue']
        }
        
        content_lower = content.lower()
        identified_topics = []
        
        for topic, keywords in topic_keywords.items():
            keyword_count = sum(content_lower.count(keyword) for keyword in keywords)
            if keyword_count > 2:  # Topic mentioned multiple times
                identified_topics.append(topic)
        
        return identified_topics[:5]  # Return top 5 topics
    
    def _assess_difficulty(self, content: str) -> str:
        """Assess difficulty level based on content complexity."""
        # Simple heuristic based on vocabulary and structure
        words = content.split()
        
        # Calculate average word length
        avg_word_length = sum(len(word) for word in words) / len(words)
        
        # Count complex terms
        complex_terms = ['implementation', 'optimization', 'architecture', 'polymorphism', 
                        'encapsulation', 'abstraction', 'inheritance', 'algorithm']
        complex_count = sum(content.lower().count(term) for term in complex_terms)
        
        # Count sentences and calculate average sentence length
        sentences = re.split(r'[.!?]+', content)
        avg_sentence_length = len(words) / len(sentences) if sentences else 0
        
        # Simple scoring
        score = 0
        if avg_word_length > 5:
            score += 1
        if complex_count > 10:
            score += 1
        if avg_sentence_length > 20:
            score += 1
        
        if score >= 2:
            return "advanced"
        elif score == 1:
            return "intermediate"
        else:
            return "beginner"
    
    def _build_word_index(self) -> None:
        """Build inverted index for fast text search."""
        self.word_index = {}
        
        for book_id, sections in self.sections.items():
            for section_id, section in sections.items():
                words = re.findall(r'\b\w+\b', section.content.lower())
                
                for word in words:
                    if len(word) > 2:  # Skip very short words
                        if word not in self.word_index:
                            self.word_index[word] = []
                        
                        # Avoid duplicates
                        location = (book_id, section_id)
                        if location not in self.word_index[word]:
                            self.word_index[word].append(location)
        
        logger.info(f"Built word index with {len(self.word_index)} unique words")
    
    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        """Search for content across all books."""
        query_words = re.findall(r'\b\w+\b', query.lower())
        
        if not query_words:
            return []
        
        # Find sections containing query words
        section_scores = {}
        
        for word in query_words:
            if word in self.word_index:
                for book_id, section_id in self.word_index[word]:
                    key = (book_id, section_id)
                    section_scores[key] = section_scores.get(key, 0) + 1
        
        # Sort by relevance score
        sorted_sections = sorted(section_scores.items(), key=lambda x: x[1], reverse=True)
        
        results = []
        for (book_id, section_id), score in sorted_sections[:limit]:
            section = self.sections[book_id][section_id]
            book = self.books[book_id]
            
            # Create content snippet with highlighted matches
            snippet = self._create_snippet(section.content, query_words)
            
            result = SearchResult(
                book_id=book_id,
                section_id=section_id,
                section_title=f"{book.title} - {section.title}",
                content_snippet=snippet,
                relevance_score=score / len(query_words)  # Normalize by query length
            )
            
            results.append(result)
        
        return results
    
    def _create_snippet(self, content: str, query_words: List[str], snippet_length: int = 200) -> str:
        """Create a snippet of content with query words highlighted."""
        # Find first occurrence of any query word
        content_lower = content.lower()
        first_match_pos = len(content)
        
        for word in query_words:
            pos = content_lower.find(word)
            if pos != -1 and pos < first_match_pos:
                first_match_pos = pos
        
        # Create snippet around first match
        start_pos = max(0, first_match_pos - snippet_length // 2)
        end_pos = min(len(content), start_pos + snippet_length)
        
        snippet = content[start_pos:end_pos]
        
        # Add ellipsis if truncated
        if start_pos > 0:
            snippet = "..." + snippet
        if end_pos < len(content):
            snippet = snippet + "..."
        
        return snippet
    
    def get_book_metadata(self, book_id: str) -> Optional[BookMetadata]:
        """Get metadata for a specific book."""
        return self.books.get(book_id)
    
    def get_book_sections(self, book_id: str) -> Dict[str, BookSection]:
        """Get all sections for a specific book."""
        return self.sections.get(book_id, {})
    
    def get_section_content(self, book_id: str, section_id: str) -> Optional[BookSection]:
        """Get content for a specific section."""
        if book_id in self.sections:
            return self.sections[book_id].get(section_id)
        return None
    
    def get_books_by_topic(self, topic: str) -> List[BookMetadata]:
        """Get books that cover a specific topic."""
        matching_books = []
        
        for book in self.books.values():
            if topic.lower() in [t.lower() for t in book.topics]:
                matching_books.append(book)
        
        return sorted(matching_books, key=lambda x: x.title)
    
    def get_reading_recommendations(self, user_topics: List[str], difficulty: str = "any") -> List[BookMetadata]:
        """Get book recommendations based on user interests."""
        recommendations = []
        
        for book in self.books.values():
            # Check topic match
            topic_match = any(topic.lower() in [t.lower() for t in book.topics] for topic in user_topics)
            
            # Check difficulty match
            difficulty_match = difficulty == "any" or book.difficulty_level == difficulty
            
            if topic_match and difficulty_match:
                recommendations.append(book)
        
        # Sort by relevance (number of matching topics)
        def relevance_score(book):
            return sum(1 for topic in user_topics if topic.lower() in [t.lower() for t in book.topics])
        
        recommendations.sort(key=relevance_score, reverse=True)
        return recommendations
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get comprehensive system statistics."""
        total_books = len(self.books)
        total_sections = sum(len(sections) for sections in self.sections.values())
        total_words = sum(book.total_words for book in self.books.values())
        
        # Topics distribution
        all_topics = []
        for book in self.books.values():
            all_topics.extend(book.topics)
        topic_counts = Counter(all_topics)
        
        # Difficulty distribution
        difficulty_counts = Counter(book.difficulty_level for book in self.books.values())
        
        return {
            "total_books": total_books,
            "total_sections": total_sections,
            "total_words": total_words,
            "average_words_per_book": total_words / total_books if total_books > 0 else 0,
            "topics_distribution": dict(topic_counts.most_common(10)),
            "difficulty_distribution": dict(difficulty_counts),
            "indexed_words": len(self.word_index),
            "average_reading_time_minutes": sum(book.reading_time_minutes for book in self.books.values()) / total_books if total_books > 0 else 0
        }
    
    def export_book_summary(self, book_id: str) -> Optional[Dict[str, Any]]:
        """Export a comprehensive summary of a book."""
        if book_id not in self.books:
            return None
        
        book = self.books[book_id]
        sections = self.sections[book_id]
        
        return {
            "metadata": {
                "book_id": book.book_id,
                "title": book.title,
                "total_words": book.total_words,
                "reading_time_minutes": book.reading_time_minutes,
                "topics": book.topics,
                "difficulty_level": book.difficulty_level,
                "processed_at": book.processed_at.isoformat()
            },
            "structure": {
                "sections_count": len(sections),
                "chapters": [
                    {
                        "section_id": section.section_id,
                        "title": section.title,
                        "word_count": section.word_count,
                        "subsections": section.subsections
                    }
                    for section in sections.values() if section.level == 1
                ]
            },
            "content_summary": {
                "word_frequency": self._get_word_frequency(book_id),
                "key_concepts": self._extract_key_concepts(book_id)
            }
        }
    
    def _get_word_frequency(self, book_id: str, top_n: int = 20) -> Dict[str, int]:
        """Get word frequency for a specific book."""
        if book_id not in self.sections:
            return {}
        
        all_words = []
        for section in self.sections[book_id].values():
            words = re.findall(r'\b\w+\b', section.content.lower())
            all_words.extend(words)
        
        # Filter out common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should', 'could', 'can', 'may', 'might', 'this', 'that', 'these', 'those'}
        
        filtered_words = [word for word in all_words if len(word) > 3 and word not in stop_words]
        word_counts = Counter(filtered_words)
        
        return dict(word_counts.most_common(top_n))
    
    def _extract_key_concepts(self, book_id: str) -> List[str]:
        """Extract key concepts from a book."""
        word_freq = self._get_word_frequency(book_id, 50)
        
        # Identify technical terms and important concepts
        key_concepts = []
        technical_indicators = ['programming', 'algorithm', 'method', 'technique', 'principle', 'concept', 'pattern', 'structure']
        
        for word, count in word_freq.items():
            if count > 3 and (len(word) > 6 or any(indicator in word for indicator in technical_indicators)):
                key_concepts.append(word)
        
        return key_concepts[:15]


# Global interpreter instance
book_interpreter = BookInterpreter()


def get_book_interpreter() -> BookInterpreter:
    """Get the global book interpreter instance."""
    return book_interpreter


if __name__ == "__main__":
    # Demo the book interpreter functionality
    print("=== Fast Track Academy - Scanned Books Interpreter Demo ===")
    
    interpreter = get_book_interpreter()
    
    # Show loaded books
    print(f"\nLoaded Books: {len(interpreter.books)}")
    for book_id, book in interpreter.books.items():
        print(f"- {book.title} ({book.total_words} words, {book.sections_count} sections)")
        print(f"  Topics: {', '.join(book.topics)}")
        print(f"  Difficulty: {book.difficulty_level}")
        print(f"  Reading time: {book.reading_time_minutes} minutes")
    
    # Search functionality
    print("\nSearch Results for 'learning':")
    search_results = interpreter.search("learning", limit=3)
    for result in search_results:
        print(f"- {result.section_title} (Score: {result.relevance_score:.2f})")
        print(f"  {result.content_snippet[:100]}...")
    
    # Topic-based recommendations
    print(f"\nBooks on 'programming':")
    programming_books = interpreter.get_books_by_topic("programming")
    for book in programming_books:
        print(f"- {book.title} ({book.difficulty_level})")
    
    # System statistics
    print("\nSystem Statistics:")
    stats = interpreter.get_system_stats()
    print(json.dumps(stats, indent=2))
    
    # Export book summary
    if interpreter.books:
        first_book_id = list(interpreter.books.keys())[0]
        print(f"\nBook Summary for '{interpreter.books[first_book_id].title}':")
        summary = interpreter.export_book_summary(first_book_id)
        if summary:
            print(f"- Sections: {summary['structure']['sections_count']}")
            print(f"- Key concepts: {', '.join(summary['content_summary']['key_concepts'][:5])}")