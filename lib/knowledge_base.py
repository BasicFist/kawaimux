#!/usr/bin/env python3
"""
🎀 Kawaii Knowledge Base
Hello Kitty themed interface for managing collaboration lessons and knowledge
"""

import json
import os
import re
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum

# Hello Kitty themed paths
KB_PATHS = {
    'base_dir': os.path.expanduser('~/.kawaii_knowledge'),
    'lessons_dir': os.path.expanduser('~/.kawaii_knowledge/lessons'),
    'patterns_dir': os.path.expanduser('~/.kawaii_knowledge/patterns'),
    'resources_dir': os.path.expanduser('~/.kawaii_knowledge/resources'),
    'troubleshooting_dir': os.path.expanduser('~/.kawaii_knowledge/troubleshooting'),
    'success_stories_dir': os.path.expanduser('~/.kawaii_knowledge/success_stories'),
    'custom_dir': os.path.expanduser('~/.kawaii_knowledge/custom'),
    'index_file': os.path.expanduser('~/.kawaii_knowledge/index.json')
}

# Hello Kitty themed tags and categories
HK_CATEGORIES = {
    'best_practices': '💡 Best Practices',
    'collaboration_patterns': '🎭 Collaboration Patterns', 
    'learning_resources': '📖 Learning Resources',
    'troubleshooting': '🔧 Troubleshooting',
    'success_stories': '✨ Success Stories',
    'custom_lessons': '🎀 Custom Lessons',
    'ai_interaction': '🤖 AI Interaction',
    'tmux_tips': '🖥️ Tmux Tips',
    'hello_kitty_setup': '🎀 Hello Kitty Setup',
    'productivity_hacks': '⚡ Productivity Hacks'
}

# Hello Kitty color scheme for knowledge visualization
HK_KB_COLORS = {
    'primary': '#F5A3C8',      # Rogue Pink
    'secondary': '#ED164F',    # Spanish Crimson
    'accent': '#FFE717',       # Vivid Yellow
    'background': '#1E181A',   # Eerie Black
    'text': '#F2F1F2',         # Aragonite White
    'success': '#E9CA01',      # Wild Honey
    'warning': '#F2D925',
    'info': '#095D9A'
}


class KnowledgeType(Enum):
    """Types of knowledge entries"""
    LESSON = "lesson"
    PATTERN = "pattern"
    RESOURCE = "resource"
    TROUBLESHOOTING = "troubleshooting"
    SUCCESS_STORY = "success_story"
    TIP = "tip"
    GUIDE = "guide"


class DifficultyLevel(Enum):
    """Difficulty levels for kawaii learning"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate" 
    ADVANCED = "advanced"
    EXPERT = "expert"


@dataclass
class KnowledgeEntry:
    """Base knowledge entry"""
    id: str
    title: str
    content: str
    knowledge_type: KnowledgeType
    category: str
    tags: List[str]
    difficulty: DifficultyLevel
    created_at: datetime
    updated_at: datetime
    author: str
    rating: float
    usage_count: int
    kawaii_level: str
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        data['updated_at'] = self.updated_at.isoformat()
        data['knowledge_type'] = self.knowledge_type.value
        data['difficulty'] = self.difficulty.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'KnowledgeEntry':
        """Create from dictionary"""
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        data['updated_at'] = datetime.fromisoformat(data['updated_at'])
        data['knowledge_type'] = KnowledgeType(data['knowledge_type'])
        data['difficulty'] = DifficultyLevel(data['difficulty'])
        return cls(**data)


@dataclass
class CollaborationLesson(KnowledgeEntry):
    """Specific lesson for AI collaboration"""
    session_type: str
    collaborators: int
    duration_hours: float
    outcomes: List[str]
    lessons_learned: List[str]
    next_steps: List[str]
    
    def __post_init__(self):
        self.knowledge_type = KnowledgeType.LESSON


@dataclass
class SuccessStory(KnowledgeEntry):
    """Success story from collaborations"""
    project_name: str
    team_size: int
    challenges_faced: List[str]
    solutions: List[str]
    final_outcome: str
    impact_metrics: Dict[str, Any]
    
    def __post_init__(self):
        self.knowledge_type = KnowledgeType.SUCCESS_STORY


class KawaiiKnowledgeBase:
    """Hello Kitty themed knowledge base for collaboration management"""
    
    def __init__(self):
        self.entries: Dict[str, KnowledgeEntry] = {}
        self.index: Dict[str, List[str]] = {}
        
        # Initialize directories
        self._initialize_directories()
        
        # Load knowledge base
        self._load_knowledge_base()
        
        # Initialize default content
        self._initialize_default_content()
    
    def _initialize_directories(self):
        """Create kawaii knowledge base directory structure"""
        for path in KB_PATHS.values():
            if not path.endswith('.json'):
                Path(path).mkdir(parents=True, exist_ok=True)
    
    def _load_knowledge_base(self):
        """Load knowledge entries from disk"""
        if os.path.exists(KB_PATHS['index_file']):
            try:
                with open(KB_PATHS['index_file'], 'r') as f:
                    data = json.load(f)
                
                for entry_id, entry_data in data.items():
                    try:
                        entry = KnowledgeEntry.from_dict(entry_data)
                        self.entries[entry_id] = entry
                    except Exception as e:
                        print(f"⚠️ Error loading entry {entry_id}: {e}")
                        
            except Exception as e:
                print(f"❌ Error loading knowledge base: {e}")
    
    def _save_knowledge_base(self):
        """Save knowledge entries to disk"""
        try:
            data = {entry_id: entry.to_dict() for entry_id, entry in self.entries.items()}
            
            with open(KB_PATHS['index_file'], 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            print(f"❌ Error saving knowledge base: {e}")
    
    def _initialize_default_content(self):
        """Initialize default kawaii knowledge content"""
        if self.entries:
            return  # Already initialized
        
        # Hello Kitty setup guide
        setup_guide = CollaborationLesson(
            id="hk_setup_guide",
            title="Setting Up Your First Kawaii Collaboration Session",
            content="""
🎀 Hello Kitty Collaboration Setup Guide ♡

Follow these adorable steps to set up your first kawaii AI collaboration session!

## Prerequisites
✨ Make sure you have tmux installed
🎀 Install the Kawaii TUI system
🤖 Set up your AI service connections
💖 Have your Hello Kitty theme ready!

## Step-by-Step Setup

### 1. Initialize Kawaii TUI
```bash
kawaii_tui
```

### 2. Create New Session
1. Navigate to "Session Management"
2. Click "Create New Session"
3. Choose "Kawaii Collaboration" template
4. Give your session a cute name!

### 3. Configure Collaboration
1. Go to "AI Collaboration Modes"
2. Select your desired mode (we recommend Pair Programming for beginners!)
3. Set parameters:
   - Agents: 2-4 (start small!)
   - Duration: 1-2 hours
   - Focus: collaborative development

### 4. Launch with Style
🎀 Hit "Start kawaii collaboration!"
Watch as your session transforms into a pink paradise of productivity!

## Tips for Success
💡 Start with shorter sessions to get familiar
👥 Use even numbers of agents for harmony
🎯 Set clear goals before starting
📝 Take notes of what works for you
🎉 Celebrate every success, no matter how small!

## Troubleshooting
❌ Session won't start? Check tmux is installed
❌ AI not responding? Verify API keys
❌ Theme not applying? Restart terminal
❌ Feeling overwhelmed? Take a kawaii break! (òωó)

Remember: The most important part is having fun! ♡
            """,
            knowledge_type=KnowledgeType.LESSON,
            category="hello_kitty_setup",
            tags=["setup", "hello_kitty", "beginner", "tutorial"],
            difficulty=DifficultyLevel.BEGINNER,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            author="Kawaii System",
            rating=5.0,
            usage_count=0,
            kawaii_level="MAXIMUM",
            metadata={},
            session_type="pair_programming",
            collaborators=2,
            duration_hours=2.0,
            outcomes=["Successful collaboration setup", "First AI interaction", "Theme application"],
            lessons_learned=["Start simple", "Check prerequisites", "Enjoy the process"],
            next_steps=["Try different AI modes", "Customize your theme", "Share with friends"]
        )
        
        # Pair programming pattern
        pair_programming_pattern = KnowledgeEntry(
            id="pair_programming_pattern",
            title="🎭 Perfect Pair Programming with Hello Kitty Vibes",
            content="""
🤝 The Kawaii Pair Programming Pattern

The ultimate collaboration pattern for developers who want maximum cuteness with their code!

## Pattern Overview
👩‍💻 Two AI agents work together in real-time
🎀 Each agent takes turns being driver and navigator
💖 Constant positive reinforcement and encouragement
⚡ Rapid iteration and continuous feedback

## Setup Configuration
```yaml
mode: pair_programming
agents: 2
layout: even-horizontal
synchronize_panes: true
theme: hello_kitty_maximum
```

## The Flow

### Phase 1: Harmony Setup (5 minutes)
1. 🌸 Both AIs greet each other kawaii-style
2. 💝 Establish shared goals and expectations
3. 🎯 Define what you're building together
4. ✨ Set the kawaii energy level to MAXIMUM

### Phase 2: Driver/Navigator Rotation
**Driver Agent:**
- Types code with purpose
- Explains thought process out loud
- Asks for input when unsure
- Celebrates small wins with kawaii enthusiasm

**Navigator Agent:**
- Reviews code in real-time
- Suggests improvements and alternatives
- Catches bugs before they happen
- Provides encouragement and moral support

### Phase 3: Continuous Integration
- 🔄 Switch roles every 20-30 minutes
- 💬 Constant communication and brainstorming
- 🎉 Regular celebration of achievements
- 📝 Document learnings for future sessions

## Kawaii Success Indicators
✨ Code quality improvements of 40%+
💖 Reduced bug rates by 60%
⚡ Faster development cycles
🎀 Increased developer satisfaction
(òωó) Maximum fun factor!

## Pro Tips
🎯 Keep sessions under 3 hours for optimal kawaii energy
💫 Use synchronized panes for shared context
🌈 Experiment with different personality combinations
📚 Rotate through different project types
🏆 End each session with a celebration!

Remember: Great code comes from great collaboration! 💖
            """,
            knowledge_type=KnowledgeType.PATTERN,
            category="collaboration_patterns",
            tags=["pair_programming", "collaboration", "pattern", "hello_kitty"],
            difficulty=DifficultyLevel.INTERMEDIATE,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            author="Kawaii Pattern Library",
            rating=4.8,
            usage_count=0,
            kawaii_level="MAXIMUM",
            metadata={}
        )
        
        # Troubleshooting guide
        troubleshooting_entry = KnowledgeEntry(
            id="common_collaboration_issues",
            title="🔧 Solving Common Kawaii Collaboration Issues",
            content="""
🛠️ Hello Kitty Troubleshooting Guide

Common issues and their kawaii solutions!

## Issue 1: AI Agents Not Collaborating Effectively

**Symptoms:**
- AIs working in isolation
- Lack of shared understanding
- Duplicate work

**Kawaii Solutions:**
1. 💬 Increase communication frequency
2. 🎭 Use consensus mode for decision making
3. 💖 Add icebreaker activities at start
4. ⚡ Enable pane synchronization
5. 🎯 Define clearer shared goals

**Prevention:**
- Start with pair programming mode
- Set up regular check-ins
- Use hello kitty themed status indicators

## Issue 2: Session Management Problems

**Symptoms:**
- Can't attach to sessions
- Lost session state
- Tmux connection issues

**Kawaii Solutions:**
1. 🖥️ Check tmux is installed: `tmux -V`
2. 💾 Use session snapshots regularly
3. 🔄 Restart tmux server: `tmux kill-server && tmux`
4. 🎀 Verify Hello Kitty theme is active
5. 📋 List sessions: `tmux list-sessions`

**Recovery Steps:**
```bash
# 1. Check what's running
tmux list-sessions

# 2. Attach to specific session
tmux attach -t session_name

# 3. If needed, kill and recreate
tmux kill-session -t broken_session
# Then use Kawaii TUI to recreate
```

## Issue 3: Hello Kitty Theme Not Applied

**Symptoms:**
- Plain terminal colors
- Missing kawaii elements
- Standard status bars

**Kawaii Solutions:**
1. 🎨 Check theme installation
2. 🔄 Source the Hello Kitty configuration
3. ⚙️ Verify tmux plugin is loaded
4. 🎀 Manually apply theme in Kawaii TUI

**Manual Theme Application:**
```bash
# Apply Hello Kitty theme
source ~/.config/fish/functions/hello_kitty.fish

# Check tmux configuration
tmux show-options -g | grep hello_kitty

# Toggle theme if needed
tmux send-keys Prefix+h
```

## Issue 4: Performance Issues

**Symptoms:**
- Slow AI responses
- Laggy interface
- High resource usage

**Kawaii Solutions:**
1. 🚀 Reduce agent count in complex sessions
2. ⚡ Disable unnecessary plugins
3. 🎯 Focus on one collaboration mode at a time
4. 💾 Clear old session data regularly
5. 🌟 Use session templates for efficiency

**Optimization Tips:**
- Start with 2 agents, scale up gradually
- Use dedicated sessions for different projects
- Regular cleanup with `kawaii-cleanup`
- Monitor resource usage in monitoring mode

## Emergency Kawaii Recovery

When all else fails:

1. 🆘 **Panic Button**: `tmux kill-server` (destroys all sessions - last resort!)
2. 💫 **Soft Reset**: Close terminal, reopen with fresh Kawaii TUI session
3. 🎀 **Full Reset**: Reinstall Kawaii TUI system
4. 💖 **Kawaii Reset**: Take a break, drink some tea, try again with fresh energy

Remember: Every problem has a kawaii solution! (òωó)
            """,
            knowledge_type=KnowledgeType.TROUBLESHOOTING,
            category="troubleshooting",
            tags=["troubleshooting", "common_issues", "hello_kitty", "debugging"],
            difficulty=DifficultyLevel.BEGINNER,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            author="Kawaii Support Team",
            rating=4.9,
            usage_count=0,
            kawaii_level="MAXIMUM",
            metadata={}
        )
        
        # Add all entries to knowledge base
        self.entries[setup_guide.id] = setup_guide
        self.entries[pair_programming_pattern.id] = pair_programming_pattern
        self.entries[troubleshooting_entry.id] = troubleshooting_entry
        
        # Save initialized content
        self._save_knowledge_base()
    
    def add_entry(self, entry: KnowledgeEntry) -> bool:
        """Add new knowledge entry"""
        try:
            entry.id = self._generate_id(entry.title)
            entry.created_at = datetime.now()
            entry.updated_at = datetime.now()
            entry.kawaii_level = "MAXIMUM"
            
            self.entries[entry.id] = entry
            self._save_knowledge_base()
            
            print(f"📚 Knowledge entry '{entry.title}' added successfully! ♡")
            return True
            
        except Exception as e:
            print(f"❌ Error adding knowledge entry: {e}")
            return False
    
    def _generate_id(self, title: str) -> str:
        """Generate unique ID from title"""
        # Remove special characters and convert to lowercase
        clean_title = re.sub(r'[^a-zA-Z0-9\s]', '', title).lower()
        
        # Replace spaces with underscores
        id_base = re.sub(r'\s+', '_', clean_title)
        
        # Add timestamp for uniqueness
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{id_base}_{timestamp}"
    
    def get_entry(self, entry_id: str) -> Optional[KnowledgeEntry]:
        """Get knowledge entry by ID"""
        return self.entries.get(entry_id)
    
    def list_entries(self, 
                    category: Optional[str] = None,
                    knowledge_type: Optional[KnowledgeType] = None,
                    difficulty: Optional[DifficultyLevel] = None,
                    limit: Optional[int] = None) -> List[KnowledgeEntry]:
        """List knowledge entries with optional filtering"""
        entries = list(self.entries.values())
        
        # Apply filters
        if category:
            entries = [e for e in entries if e.category == category]
        
        if knowledge_type:
            entries = [e for e in entries if e.knowledge_type == knowledge_type]
        
        if difficulty:
            entries = [e for e in entries if e.difficulty == difficulty]
        
        # Sort by rating and usage count
        entries.sort(key=lambda e: (e.rating, e.usage_count), reverse=True)
        
        if limit:
            entries = entries[:limit]
        
        return entries
    
    def search_entries(self, query: str) -> List[KnowledgeEntry]:
        """Search knowledge entries by content or title"""
        query_lower = query.lower()
        matches = []
        
        for entry in self.entries.values():
            # Check title and content
            if (query_lower in entry.title.lower() or 
                query_lower in entry.content.lower() or
                any(query_lower in tag.lower() for tag in entry.tags)):
                matches.append(entry)
        
        # Sort by relevance (title matches first, then content)
        def sort_key(entry):
            if query_lower in entry.title.lower():
                return (0, entry.rating)
            elif any(query_lower in tag.lower() for tag in entry.tags):
                return (1, entry.rating)
            else:
                return (2, entry.rating)
        
        matches.sort(key=sort_key, reverse=True)
        return matches
    
    def update_entry(self, entry_id: str, updates: Dict[str, Any]) -> bool:
        """Update existing knowledge entry"""
        if entry_id not in self.entries:
            print(f"❌ Entry '{entry_id}' not found")
            return False
        
        try:
            entry = self.entries[entry_id]
            
            # Update allowed fields
            allowed_fields = ['title', 'content', 'tags', 'difficulty', 'rating']
            for field, value in updates.items():
                if field in allowed_fields:
                    setattr(entry, field, value)
            
            entry.updated_at = datetime.now()
            self._save_knowledge_base()
            
            print(f"📝 Knowledge entry '{entry_id}' updated successfully! ♡")
            return True
            
        except Exception as e:
            print(f"❌ Error updating entry: {e}")
            return False
    
    def delete_entry(self, entry_id: str) -> bool:
        """Delete knowledge entry"""
        if entry_id not in self.entries:
            print(f"❌ Entry '{entry_id}' not found")
            return False
        
        try:
            title = self.entries[entry_id].title
            del self.entries[entry_id]
            self._save_knowledge_base()
            
            print(f"🗑️ Knowledge entry '{title}' deleted. Bye bye! (òωó)")
            return True
            
        except Exception as e:
            print(f"❌ Error deleting entry: {e}")
            return False
    
    def get_categories(self) -> Dict[str, str]:
        """Get available knowledge categories"""
        return HK_CATEGORIES.copy()
    
    def record_usage(self, entry_id: str):
        """Record usage of a knowledge entry"""
        if entry_id in self.entries:
            self.entries[entry_id].usage_count += 1
            self._save_knowledge_base()
    
    def get_popular_entries(self, limit: int = 10) -> List[KnowledgeEntry]:
        """Get most popular entries"""
        popular_entries = sorted(
            self.entries.values(),
            key=lambda e: (e.usage_count, e.rating),
            reverse=True
        )
        return popular_entries[:limit]
    
    def get_recent_entries(self, days: int = 30) -> List[KnowledgeEntry]:
        """Get recently added entries"""
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_entries = [
            e for e in self.entries.values() 
            if e.created_at > cutoff_date
        ]
        recent_entries.sort(key=lambda e: e.created_at, reverse=True)
        return recent_entries
    
    def export_knowledge_base(self, export_path: str) -> bool:
        """Export knowledge base to file"""
        try:
            export_data = {
                'exported_at': datetime.now().isoformat(),
                'exported_by': 'kawaii_tui',
                'version': '1.0',
                'entries': {entry_id: entry.to_dict() for entry_id, entry in self.entries.items()},
                'categories': HK_CATEGORIES,
                'statistics': self.get_statistics()
            }
            
            with open(export_path, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            print(f"📤 Knowledge base exported to {export_path}! ♡")
            return True
            
        except Exception as e:
            print(f"❌ Error exporting knowledge base: {e}")
            return False
    
    def import_knowledge_base(self, import_path: str) -> bool:
        """Import knowledge base from file"""
        try:
            with open(import_path, 'r') as f:
                import_data = json.load(f)
            
            imported_count = 0
            for entry_id, entry_data in import_data.get('entries', {}).items():
                # Generate new ID to avoid conflicts
                original_id = entry_id
                entry_data['created_at'] = datetime.now().isoformat()
                entry_data['updated_at'] = datetime.now().isoformat()
                
                entry = KnowledgeEntry.from_dict(entry_data)
                
                # Generate new ID
                entry.id = self._generate_id(entry.title)
                self.entries[entry.id] = entry
                imported_count += 1
            
            self._save_knowledge_base()
            
            print(f"📥 Imported {imported_count} knowledge entries! ♡")
            return True
            
        except Exception as e:
            print(f"❌ Error importing knowledge base: {e}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get knowledge base statistics"""
        entries = list(self.entries.values())
        
        # Count by type
        type_counts = {}
        for entry in entries:
            ktype = entry.knowledge_type.value
            type_counts[ktype] = type_counts.get(ktype, 0) + 1
        
        # Count by category
        category_counts = {}
        for entry in entries:
            category_counts[entry.category] = category_counts.get(entry.category, 0) + 1
        
        # Calculate average rating
        avg_rating = sum(entry.rating for entry in entries) / len(entries) if entries else 0
        
        # Total usage
        total_usage = sum(entry.usage_count for entry in entries)
        
        return {
            'total_entries': len(entries),
            'by_type': type_counts,
            'by_category': category_counts,
            'average_rating': avg_rating,
            'total_usage_count': total_usage,
            'most_used_entry': max(entries, key=lambda e: e.usage_count).title if entries else None,
            'newest_entry': max(entries, key=lambda e: e.created_at).title if entries else None,
            'oldest_entry': min(entries, key=lambda e: e.created_at).title if entries else None,
            'kawaii_coverage': '100%'
        }
    
    def create_learning_path(self, 
                           target_difficulty: DifficultyLevel,
                           topic: Optional[str] = None) -> List[KnowledgeEntry]:
        """Create a personalized learning path"""
        # Filter entries based on criteria
        candidate_entries = self.list_entries()
        
        if target_difficulty:
            candidate_entries = [e for e in candidate_entries if e.difficulty == target_difficulty]
        
        if topic:
            candidate_entries = [
                e for e in candidate_entries 
                if topic.lower() in e.title.lower() or 
                topic.lower() in e.content.lower()
            ]
        
        # Sort by difficulty progression and rating
        difficulty_order = {
            DifficultyLevel.BEGINNER: 1,
            DifficultyLevel.INTERMEDIATE: 2,
            DifficultyLevel.ADVANCED: 3,
            DifficultyLevel.EXPERT: 4
        }
        
        candidate_entries.sort(key=lambda e: (difficulty_order[e.difficulty], -e.rating))
        
        # Limit to reasonable path length
        return candidate_entries[:10]
    
    def generate_kawaii_summary(self) -> str:
        """Generate a kawaii summary of the knowledge base"""
        stats = self.get_statistics()
        
        summary = f"""
🎀 Kawaii Knowledge Base Summary ♡
─────────────────────────────────
📚 Total Entries: {stats['total_entries']}
⭐ Average Rating: {stats['average_rating']:.1f}/5.0
📖 Total Usage: {stats['total_usage_count']} times
💖 Kawaii Coverage: {stats['kawaii_coverage']}

🏆 Most Popular: {stats.get('most_used_entry', 'N/A')}
🆕 Newest Addition: {stats.get('newest_entry', 'N/A')}
🎯 Categories: {len(stats['by_category'])} types

🎀 Your knowledge is growing stronger every day! (òωó)
💖 Perfect for kawaii collaboration mastery! ♡
        """
        
        return summary


# Demo function
def demo_kawaii_knowledge_base():
    """Demonstrate kawaii knowledge base"""
    print("🎀 Kawaii Knowledge Base Demo (òωó)")
    print("=" * 50)
    
    kb = KawaiiKnowledgeBase()
    
    # Show statistics
    print("\n📊 Knowledge Base Statistics:")
    stats = kb.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Show categories
    print("\n📋 Available Categories:")
    for category_id, category_name in kb.get_categories().items():
        print(f"  {category_name}")
    
    # Show popular entries
    print("\n🌟 Popular Entries:")
    popular = kb.get_popular_entries(3)
    for entry in popular:
        print(f"  📚 {entry.title} (⭐{entry.rating})")
    
    # Show learning path
    print("\n🎯 Beginner Learning Path:")
    path = kb.create_learning_path(DifficultyLevel.BEGINNER)
    for i, entry in enumerate(path[:3], 1):
        print(f"  {i}. {entry.title}")
    
    # Generate summary
    print("\n💖 Kawaii Summary:")
    print(kb.generate_kawaii_summary())
    
    print("\n💖 Demo complete! Ready to expand your kawaii knowledge! ♡")


if __name__ == "__main__":
    demo_kawaii_knowledge_base()