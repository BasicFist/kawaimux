#!/usr/bin/env python3
"""
🎀 Kawaii Workflow Templates
Hello Kitty themed templates for common AI collaboration scenarios
"""

import json
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum

# Hello Kitty themed paths
WT_PATHS = {
    'templates_dir': os.path.expanduser('~/.kawaii_workflow_templates'),
    'shared_dir': os.path.expanduser('~/.kawaii_shared_templates'),
    'custom_dir': os.path.expanduser('~/.kawaii_custom_templates')
}

# Workflow categories
WF_CATEGORIES = {
    'development': '💻 Development Workflows',
    'collaboration': '🤝 Collaboration Workflows',
    'learning': '📚 Learning Workflows',
    'creative': '🎨 Creative Workflows',
    'analysis': '📊 Analysis Workflows',
    'presentation': '🎭 Presentation Workflows',
    'custom': '🎀 Custom Workflows'
}

# Hello Kitty color palette for workflow visualization
HK_WF_COLORS = {
    'primary': '#F5A3C8',      # Rogue Pink
    'secondary': '#ED164F',    # Spanish Crimson
    'accent': '#FFE717',       # Vivid Yellow
    'background': '#1E181A',   # Eerie Black
    'text': '#F2F1F2',         # Aragonite White
    'success': '#E9CA01',      # Wild Honey
    'info': '#095D9A'
}


class WorkflowComplexity(Enum):
    """Workflow complexity levels"""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    ADVANCED = "advanced"


class WorkflowType(Enum):
    """Types of workflow templates"""
    COLLABORATION = "collaboration"
    DEVELOPMENT = "development"
    LEARNING = "learning"
    CREATIVE = "creative"
    ANALYSIS = "analysis"
    PRESENTATION = "presentation"
    CUSTOM = "custom"


@dataclass
class WorkflowStep:
    """Individual step in a workflow"""
    id: str
    name: str
    description: str
    step_type: str  # 'agent_action', 'collaboration', 'decision', 'review'
    duration_minutes: int
    required_agents: int
    ai_prompt: str
    expected_outcome: str
    kawaii_message: str
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class WorkflowTemplate:
    """Complete workflow template"""
    id: str
    name: str
    description: str
    category: str
    workflow_type: WorkflowType
    complexity: WorkflowComplexity
    estimated_duration_hours: float
    required_agents: int
    steps: List[WorkflowStep]
    prerequisites: List[str]
    outcomes: List[str]
    hello_kitty_theme: bool
    tags: List[str]
    rating: float
    usage_count: int
    created_at: datetime
    updated_at: datetime
    author: str
    kawaii_level: str
    
    def to_dict(self) -> Dict:
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        data['updated_at'] = self.updated_at.isoformat()
        data['workflow_type'] = self.workflow_type.value
        data['complexity'] = self.complexity.value
        return data


class KawaiiWorkflowTemplates:
    """Hello Kitty themed workflow template system"""
    
    def __init__(self):
        self.templates: Dict[str, WorkflowTemplate] = {}
        
        # Initialize directories
        self._initialize_directories()
        
        # Load templates
        self._load_templates()
        
        # Initialize default templates
        self._initialize_default_templates()
    
    def _initialize_directories(self):
        """Create workflow template directories"""
        for path in WT_PATHS.values():
            Path(path).mkdir(parents=True, exist_ok=True)
    
    def _load_templates(self):
        """Load workflow templates from disk"""
        templates_file = os.path.join(WT_PATHS['templates_dir'], 'templates.json')
        
        if os.path.exists(templates_file):
            try:
                with open(templates_file, 'r') as f:
                    data = json.load(f)
                
                for template_id, template_data in data.items():
                    try:
                        template = self._dict_to_template(template_data)
                        self.templates[template_id] = template
                    except Exception as e:
                        print(f"⚠️ Error loading template {template_id}: {e}")
                        
            except Exception as e:
                print(f"❌ Error loading templates: {e}")
    
    def _save_templates(self):
        """Save templates to disk"""
        templates_file = os.path.join(WT_PATHS['templates_dir'], 'templates.json')
        
        try:
            data = {template_id: template.to_dict() for template_id, template in self.templates.items()}
            
            with open(templates_file, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            print(f"❌ Error saving templates: {e}")
    
    def _dict_to_template(self, data: Dict) -> WorkflowTemplate:
        """Convert dictionary to WorkflowTemplate"""
        # Convert datetime strings
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        data['updated_at'] = datetime.fromisoformat(data['updated_at'])
        
        # Convert enums
        data['workflow_type'] = WorkflowType(data['workflow_type'])
        data['complexity'] = WorkflowComplexity(data['complexity'])
        
        # Convert steps
        data['steps'] = [WorkflowStep(**step) for step in data['steps']]
        
        return WorkflowTemplate(**data)
    
    def _initialize_default_templates(self):
        """Initialize default kawaii workflow templates"""
        if self.templates:
            return  # Already initialized
        
        # Developer Pair Programming Workflow
        pair_programming_workflow = WorkflowTemplate(
            id="developer_pair_programming",
            name="👩‍💻 Developer Pair Programming Marathon",
            description="The ultimate kawaii coding collaboration experience! Perfect for building amazing software with AI friends.",
            category="development",
            workflow_type=WorkflowType.COLLABORATION,
            complexity=WorkflowComplexity.MODERATE,
            estimated_duration_hours=3.0,
            required_agents=2,
            steps=[
                WorkflowStep(
                    id="setup",
                    name="🎀 Kawaii Setup",
                    description="Initialize the collaboration environment with Hello Kitty theming",
                    step_type="agent_action",
                    duration_minutes=5,
                    required_agents=2,
                    ai_prompt="Set up the development environment and apply Hello Kitty theme. Welcome your AI partner with kawaii enthusiasm!",
                    expected_outcome="Development environment ready with kawaii styling",
                    kawaii_message="Ready for maximum coding cuteness! (òωó)",
                    metadata={}
                ),
                WorkflowStep(
                    id="project_planning",
                    name="🗺️ Project Planning Circle",
                    description="Collaboratively plan the project with both AI agents",
                    step_type="collaboration",
                    duration_minutes=20,
                    required_agents=2,
                    ai_prompt="Work together to plan the project scope, features, and architecture. Use collaborative discussion to reach agreement.",
                    expected_outcome="Clear project plan agreed upon by both agents",
                    kawaii_message="Planning together makes everything better! ♡",
                    metadata={}
                ),
                WorkflowStep(
                    id="coding_sprint",
                    name="⚡ Kawaii Coding Sprint",
                    description="Main development phase with driver/navigator rotation",
                    step_type="collaboration",
                    duration_minutes=120,
                    required_agents=2,
                    ai_prompt="Take turns being driver and navigator. Write code with purpose, review actively, and maintain kawaii energy throughout!",
                    expected_outcome="Significant progress on project features",
                    kawaii_message="Coding together is the best! 💖",
                    metadata={}
                ),
                WorkflowStep(
                    id="code_review",
                    name="🔍 Code Review Party",
                    description="Thoroughly review all code together",
                    step_type="review",
                    duration_minutes=30,
                    required_agents=2,
                    ai_prompt="Conduct comprehensive code review. Check for bugs, improvements, and ensure code quality meets kawaii standards!",
                    expected_outcome="Clean, well-reviewed codebase",
                    kawaii_message="Perfect code deserves perfect review! (òωó)",
                    metadata={}
                ),
                WorkflowStep(
                    id="celebration",
                    name="🎉 Kawaii Celebration",
                    description="Celebrate achievements and plan next steps",
                    step_type="agent_action",
                    duration_minutes=10,
                    required_agents=2,
                    ai_prompt="Celebrate your accomplishments! Document lessons learned and plan next collaboration session.",
                    expected_outcome="Positive closure with clear next steps",
                    kawaii_message="We did amazing work together! ♡",
                    metadata={}
                )
            ],
            prerequisites=["Hello Kitty theme active", "Development environment ready"],
            outcomes=["Functional software project", "Strong AI collaboration", "Learning documentation"],
            hello_kitty_theme=True,
            tags=["development", "pair_programming", "collaboration", "coding"],
            rating=5.0,
            usage_count=0,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            author="Kawaii Workflow Team",
            kawaii_level="MAXIMUM"
        )
        
        # Creative Workshop Workflow
        creative_workshop_workflow = WorkflowTemplate(
            id="creative_workshop",
            name="🎨 Creative Workshop Brainstorm",
            description="Unleash creativity with AI collaborators in a kawaii environment! Perfect for design thinking and creative projects.",
            category="creative",
            workflow_type=WorkflowType.CREATIVE,
            complexity=WorkflowComplexity.SIMPLE,
            estimated_duration_hours=2.0,
            required_agents=3,
            steps=[
                WorkflowStep(
                    id="creative_warmup",
                    name="🌸 Creative Warm-up",
                    description="Get into the kawaii creative zone",
                    step_type="agent_action",
                    duration_minutes=10,
                    required_agents=3,
                    ai_prompt="Begin with creative exercises to get minds flowing. Use kawaii enthusiasm to spark imagination!",
                    expected_outcome="All agents in creative mode",
                    kawaii_message="Creativity is flowing like kawaii magic! ♡",
                    metadata={}
                ),
                WorkflowStep(
                    id="idea_storm",
                    name="💡 Idea Storm Session",
                    description="Generate many creative ideas without judgment",
                    step_type="collaboration",
                    duration_minutes=30,
                    required_agents=3,
                    ai_prompt="Brainstorm freely and build on each other's ideas. No idea is too wild! Embrace kawaii chaos and creativity.",
                    expected_outcome="Large collection of creative ideas",
                    kawaii_message="The ideas are flowing like kawaii confetti! (òωó)",
                    metadata={}
                ),
                WorkflowStep(
                    id="idea_evaluation",
                    name="🎭 Idea Evaluation Circle",
                    description="Evaluate and refine the best ideas together",
                    step_type="decision",
                    duration_minutes=25,
                    required_agents=3,
                    ai_prompt="Discuss ideas constructively, evaluate feasibility, and choose the most promising directions.",
                    expected_outcome="Refined list of top creative concepts",
                    kawaii_message="Great ideas shine brighter when refined together! ♡",
                    metadata={}
                ),
                WorkflowStep(
                    id="concept_development",
                    name="💎 Concept Development",
                    description="Develop chosen concepts in detail",
                    step_type="collaboration",
                    duration_minutes=45,
                    required_agents=3,
                    ai_prompt="Deep dive into chosen concepts. Develop detailed plans, mockups, or prototypes collaboratively.",
                    expected_outcome="Detailed creative concepts ready for implementation",
                    kawaii_message="Concepts coming to life with kawaii perfection! (òωó)",
                    metadata={}
                )
            ],
            prerequisites=["Creative mindset", "Hello Kitty inspiration"],
            outcomes=["Detailed creative concepts", "Implementation roadmap", "Creative inspiration"],
            hello_kitty_theme=True,
            tags=["creative", "brainstorming", "design", "collaboration"],
            rating=4.9,
            usage_count=0,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            author="Kawaii Creative Team",
            kawaii_level="MAXIMUM"
        )
        
        # Ops Incident Drill Workflow (replaces teaching)
        ops_incident_workflow = WorkflowTemplate(
            id="ops_incident_drill",
            name="🚨 Ops Incident Drill",
            description="Practice a full incident lifecycle with AI responders, coordinator, and postmortem writer.",
            category="analysis",
            workflow_type=WorkflowType.ANALYSIS,
            complexity=WorkflowComplexity.ADVANCED,
            estimated_duration_hours=1.5,
            required_agents=3,
            steps=[
                WorkflowStep(
                    id="signal_intake",
                    name="📡 Signal Intake",
                    description="Gather alerts, logs, and user reports; classify severity.",
                    step_type="agent_action",
                    duration_minutes=10,
                    required_agents=3,
                    ai_prompt="Summarize active alerts, stack traces, and user reports; propose severity and initial impact surface.",
                    expected_outcome="Incident summary with severity and blast radius",
                    kawaii_message="Kitty ears perk up—let's sniff out the issue! (=^･ω･^=)",
                    metadata={}
                ),
                WorkflowStep(
                    id="triage_remediate",
                    name="🧯 Triage & Remediate",
                    description="Hypotheses, runbooks, and mitigation steps.",
                    step_type="collaboration",
                    duration_minutes=35,
                    required_agents=3,
                    ai_prompt="List top 3 hypotheses, map to runbook steps, execute mitigations safely, and track outcomes.",
                    expected_outcome="Applied mitigation with logs of actions",
                    kawaii_message="Calm paws, quick claws—let’s fix it! (ฅ'ω'ฅ)",
                    metadata={}
                ),
                WorkflowStep(
                    id="postmortem",
                    name="📑 Postmortem & Lessons",
                    description="Timeline, root cause, follow-ups, and action items.",
                    step_type="review",
                    duration_minutes=20,
                    required_agents=3,
                    ai_prompt="Compile timeline, root cause analysis, user impact, and concrete follow-ups with owners and deadlines.",
                    expected_outcome="Postmortem draft with action items",
                    kawaii_message="Every furball teaches us something nya~",
                    metadata={}
                )
            ],
            prerequisites=["Access to logs/metrics", "Runbooks available"],
            outcomes=["Postmortem draft", "Action items", "Runbook improvements"],
            hello_kitty_theme=True,
            tags=["ops", "incident", "analysis", "resilience"],
            rating=4.7,
            usage_count=0,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            author="Kawaii Reliability Team",
            kawaii_level="MAXIMUM"
        )

        # Academic Writing Sprint Workflow (replaces competition)
        story_sprint_workflow = WorkflowTemplate(
            id="academic_writing_sprint",
            name="📚 Academic Writing Sprint",
            description="Two drafting agents plus a curator produce a rigorous, cited academic section (IMRaD-friendly).",
            category="analysis",
            workflow_type=WorkflowType.ANALYSIS,
            complexity=WorkflowComplexity.MODERATE,
            estimated_duration_hours=1.2,
            required_agents=3,
            steps=[
                WorkflowStep(
                    id="claim_plan",
                    name="🎯 Claim & Outline",
                    description="Define research question/claim, scope, and outline with target section length.",
                    step_type="collaboration",
                    duration_minutes=15,
                    required_agents=3,
                    ai_prompt="Propose 2-3 research questions/claims, pick one. Produce a bullet outline with section/paragraph roles and target word counts.",
                    expected_outcome="Approved claim + outline with word budget",
                    kawaii_message="Sharp claws, sharp claims! 🐾",
                    metadata={}
                ),
                WorkflowStep(
                    id="evidence_pass",
                    name="🔎 Evidence & Citations",
                    description="Collect/verify sources, draft citation stubs (e.g., (Author, Year)), note DOI/URL.",
                    step_type="agent_action",
                    duration_minutes=20,
                    required_agents=3,
                    ai_prompt="Draft a source table: claim support, citation stub (Author, Year), DOI/URL, key quote, reliability note. Prefer peer-reviewed or reputable primary sources.",
                    expected_outcome="Source table with citation stubs and relevance notes",
                    kawaii_message="Kitties chase only the best sources! ✨",
                    metadata={}
                ),
                WorkflowStep(
                    id="draft_pass",
                    name="📝 Draft Sections",
                    description="Writer A drafts argument; Writer B drafts methods/results or counterpoint; curator checks style and cohesion.",
                    step_type="collaboration",
                    duration_minutes=35,
                    required_agents=3,
                    ai_prompt="Writer A: argument/narrative. Writer B: methods/results or counterpoint. Include citation stubs inline. Curator: enforce tone (formal), coherence, and logical flow.",
                    expected_outcome="Full draft with inline citation stubs",
                    kawaii_message="Pad with rigor, purr with clarity! (✿◠‿◠)",
                    metadata={}
                ),
                WorkflowStep(
                    id="polish_refs",
                    name="✨ Polish & References",
                    description="Curator edits for concision, clarity, hedging; assembles reference list placeholders.",
                    step_type="review",
                    duration_minutes=15,
                    required_agents=3,
                    ai_prompt="Tighten prose, add hedging where evidence is weak, enforce consistent citation style. Generate reference list stubs matching inline citations.",
                    expected_outcome="Polished academic section + reference stubs",
                    kawaii_message="Citations aligned like whiskers! 🎀",
                    metadata={}
                )
            ],
            prerequisites=["Topic/claim chosen", "Access to sources or search"],
            outcomes=["Polished academic section", "Source table", "Reference stubs"],
            hello_kitty_theme=True,
            tags=["academic", "writing", "citations", "analysis"],
            rating=4.9,
            usage_count=0,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            author="Kawaii Research Team",
            kawaii_level="MAXIMUM"
        )
        
        # Add templates to system
        # Brainstorming Burst Workflow
        brainstorm_workflow = WorkflowTemplate(
            id="brainstorm_bloom",
            name="🌸 Brainstorm Bloom",
            description="High-energy brainstorming with rapid divergence then convergence, curated by a facilitator.",
            category="creative",
            workflow_type=WorkflowType.CREATIVE,
            complexity=WorkflowComplexity.MODERATE,
            estimated_duration_hours=0.8,
            required_agents=3,
            steps=[
                WorkflowStep(
                    id="warmup",
                    name="🌷 Warmup & Framing",
                    description="Clarify problem statement, constraints, and success signals; light warmup ideas.",
                    step_type="agent_action",
                    duration_minutes=10,
                    required_agents=3,
                    ai_prompt="Restate the challenge, list constraints, define what success looks like. Generate 3 quick warmup ideas.",
                    expected_outcome="Clear brief + initial seed ideas",
                    kawaii_message="Stretch those whiskers—ideas incoming! ✨",
                    metadata={}
                ),
                WorkflowStep(
                    id="diverge",
                    name="🌠 Divergent Burst",
                    description="Timed idea storm; push for novelty and coverage; tag ideas.",
                    step_type="collaboration",
                    duration_minutes=20,
                    required_agents=3,
                    ai_prompt="In rapid rounds, propose ideas with tags (novelty, feasibility, impact). Aim for 15+ ideas, include wildcards.",
                    expected_outcome="Tagged idea list (breadth-focused)",
                    kawaii_message="Scatter the star-dust of ideas! ☆彡",
                    metadata={}
                ),
                WorkflowStep(
                    id="converge",
                    name="🎯 Converge & Rank",
                    description="Cluster, score (impact/effort/delight), shortlist top candidates.",
                    step_type="collaboration",
                    duration_minutes=15,
                    required_agents=3,
                    ai_prompt="Cluster similar ideas. Score each (Impact 1-5, Effort 1-5, Delight 1-5). Select top 3 with rationale.",
                    expected_outcome="Ranked short list with rationale",
                    kawaii_message="Pick the shiniest gems from the pile! 💎",
                    metadata={}
                ),
                WorkflowStep(
                    id="next_steps",
                    name="🧭 Next Steps",
                    description="Draft mini-briefs and owners for the top ideas.",
                    step_type="review",
                    duration_minutes=10,
                    required_agents=3,
                    ai_prompt="For each top idea, draft a mini-brief: problem, solution sketch, risks, first experiment, owner, timeline.",
                    expected_outcome="Actionable briefs for the finalists",
                    kawaii_message="Tie a ribbon on the winners and march forward! 🎀",
                    metadata={}
                ),
            ],
            prerequisites=["Problem statement", "Any constraints noted"],
            outcomes=["Ranked idea short-list", "Mini-briefs for execution"],
            hello_kitty_theme=True,
            tags=["brainstorm", "creative", "ideation", "prioritization"],
            rating=4.8,
            usage_count=0,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            author="Kawaii Ideation Team",
            kawaii_level="MAXIMUM"
        )

        # Add templates to system
        for template in [pair_programming_workflow, creative_workshop_workflow, ops_incident_workflow, story_sprint_workflow, brainstorm_workflow]:
            self.templates[template.id] = template
        
        self._save_templates()
    
    def list_templates(self, 
                      category: Optional[str] = None,
                      workflow_type: Optional[WorkflowType] = None,
                      complexity: Optional[WorkflowComplexity] = None) -> List[WorkflowTemplate]:
        """List workflow templates with optional filtering"""
        templates = list(self.templates.values())
        
        # Apply filters
        if category:
            templates = [t for t in templates if t.category == category]
        
        if workflow_type:
            templates = [t for t in templates if t.workflow_type == workflow_type]
        
        if complexity:
            templates = [t for t in templates if t.complexity == complexity]
        
        # Sort by rating and usage
        templates.sort(key=lambda t: (t.rating, t.usage_count), reverse=True)
        
        return templates
    
    def get_template(self, template_id: str) -> Optional[WorkflowTemplate]:
        """Get template by ID"""
        return self.templates.get(template_id)
    
    def create_custom_template(self, 
                             name: str,
                             description: str,
                             category: str,
                             workflow_type: WorkflowType,
                             steps: List[Dict],
                             author: str = "Custom") -> bool:
        """Create a custom workflow template"""
        try:
            template_id = self._generate_id(name)
            
            # Convert step dictionaries to WorkflowStep objects
            workflow_steps = []
            for step_data in steps:
                workflow_steps.append(WorkflowStep(**step_data))
            
            template = WorkflowTemplate(
                id=template_id,
                name=name,
                description=description,
                category=category,
                workflow_type=workflow_type,
                complexity=WorkflowComplexity.MODERATE,  # Default
                estimated_duration_hours=sum(s.duration_minutes for s in workflow_steps) / 60,
                required_agents=max(s.required_agents for s in workflow_steps),
                steps=workflow_steps,
                prerequisites=[],
                outcomes=[],
                hello_kitty_theme=True,
                tags=["custom"],
                rating=0.0,
                usage_count=0,
                created_at=datetime.now(),
                updated_at=datetime.now(),
                author=author,
                kawaii_level="CUSTOM"
            )
            
            self.templates[template_id] = template
            self._save_templates()
            
            print(f"🎨 Custom workflow '{name}' created successfully! ♡")
            return True
            
        except Exception as e:
            print(f"❌ Error creating custom template: {e}")
            return False
    
    def _generate_id(self, name: str) -> str:
        """Generate unique template ID"""
        import re
        clean_name = re.sub(r'[^a-zA-Z0-9\s]', '', name).lower()
        clean_name = re.sub(r'\s+', '_', clean_name)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{clean_name}_{timestamp}"
    
    def launch_workflow(self, 
                       template_id: str,
                       session_name: str,
                       customizations: Optional[Dict[str, Any]] = None) -> bool:
        """Launch a workflow template as a collaboration session"""
        try:
            template = self.templates.get(template_id)
            if not template:
                print(f"❌ Template '{template_id}' not found")
                return False
            
            print(f"🎬 Launching workflow: {template.name}")
            print(f"🖥️ Session: {session_name}")
            print(f"⏱️ Duration: {template.estimated_duration_hours} hours")
            print(f"🤖 Agents: {template.required_agents}")
            
            # Create tmux session
            create_cmd = [
                'tmux', 'new-session', '-d', '-s', session_name,
                '-n', f"workflow_{template.category}"
            ]
            subprocess.run(create_cmd, check=True)
            
            # Apply Hello Kitty theme
            self._apply_workflow_theme(session_name, template)
            
            # Send welcome message
            welcome_msg = f"""
🎀 Kawaii Workflow Starting! ♡
────────────────────────────────
Workflow: {template.name}
Category: {WF_CATEGORIES[template.category]}
Duration: {template.estimated_duration_hours} hours
Agents: {template.required_agents}

💖 Ready for kawaii collaboration!
            """
            
            subprocess.run([
                'tmux', 'send-keys', '-t', f'{session_name}:0',
                f'echo "{welcome_msg.strip()}"', 'Enter'
            ], check=True)
            
            # Increment usage count
            template.usage_count += 1
            template.updated_at = datetime.now()
            self._save_templates()
            
            # Display launch success
            self._display_launch_success(template, session_name)
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to launch workflow: {e}")
            return False
        except Exception as e:
            print(f"❌ Error launching workflow: {e}")
            return False
    
    def _apply_workflow_theme(self, session_name: str, template: WorkflowTemplate):
        """Apply Hello Kitty theme to workflow session"""
        theme_commands = [
            f"tmux set-option -t {session_name} status-style 'bg={HK_WF_COLORS['primary']} fg={HK_WF_COLORS['background']}'",
            f"tmux set-option -t {session_name} status-left '#[bg={HK_WF_COLORS['primary']} fg={HK_WF_COLORS['background']}]🎀 Kawaii Workflow #[default]'",
            f"tmux set-option -t {session_name} status-right '#[bg={HK_WF_COLORS['accent']} fg={HK_WF_COLORS['background']}]♡ {template.name[:15]}... #[default]'",
            f"tmux set-window-option -t {session_name} window-status-current-style 'fg={HK_WF_COLORS['accent']} bg={HK_WF_COLORS['background']} bold'",
            f"tmux set-window-option -t {session_name} window-status-style 'fg={HK_WF_COLORS['primary']} bg={HK_WF_COLORS['background']}'"
        ]
        
        for cmd in theme_commands:
            try:
                subprocess.run(cmd.split(), check=True)
            except subprocess.CalledProcessError:
                continue
    
    def _display_launch_success(self, template: WorkflowTemplate, session_name: str):
        """Display kawaii launch success message"""
        success_msg = f"""
🎬 Kawaii Workflow Launched Successfully! ♡
──────────────────────────────────────────
📋 Workflow: {template.name}
🖥️ Session: {session_name}
🎯 Category: {WF_CATEGORIES[template.category]}
⏱️ Duration: {template.estimated_duration_hours} hours
🤖 Agents: {template.required_agents}
💖 Kawaii Level: {template.kawaii_level}

🚀 Quick Commands:
• Attach: tmux attach -t {session_name}
• View workflow steps: Check knowledge base
• Get help: kawaii-help workflow

🎀 Your kawaii collaboration adventure begins now! (òωó)

Happy workflow-ing! ♡
        """
        print(success_msg)
    
    def export_template(self, template_id: str, export_path: str) -> bool:
        """Export template to file"""
        template = self.templates.get(template_id)
        if not template:
            print(f"❌ Template '{template_id}' not found")
            return False
        
        try:
            export_data = {
                'exported_at': datetime.now().isoformat(),
                'exported_by': 'kawaii_tui',
                'template': template.to_dict()
            }
            
            with open(export_path, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            print(f"📤 Template '{template.name}' exported to {export_path}! ♡")
            return True
            
        except Exception as e:
            print(f"❌ Error exporting template: {e}")
            return False
    
    def import_template(self, import_path: str) -> bool:
        """Import template from file"""
        try:
            with open(import_path, 'r') as f:
                import_data = json.load(f)
            
            template_data = import_data['template']
            template_data['created_at'] = datetime.now().isoformat()
            template_data['updated_at'] = datetime.now().isoformat()
            template_data['usage_count'] = 0
            
            # Generate new ID to avoid conflicts
            template_data['id'] = self._generate_id(template_data['name'])
            
            template = self._dict_to_template(template_data)
            self.templates[template.id] = template
            self._save_templates()
            
            print(f"📥 Template '{template.name}' imported successfully! ♡")
            return True
            
        except Exception as e:
            print(f"❌ Error importing template: {e}")
            return False
    
    def delete_template(self, template_id: str) -> bool:
        """Delete workflow template"""
        if template_id not in self.templates:
            print(f"❌ Template '{template_id}' not found")
            return False
        
        try:
            name = self.templates[template_id].name
            del self.templates[template_id]
            self._save_templates()
            
            print(f"🗑️ Workflow template '{name}' deleted. Bye bye! (òωó)")
            return True
            
        except Exception as e:
            print(f"❌ Error deleting template: {e}")
            return False
    
    def get_workflow_analytics(self) -> Dict[str, Any]:
        """Get workflow usage analytics"""
        templates = list(self.templates.values())
        
        # Calculate usage statistics
        total_usage = sum(t.usage_count for t in templates)
        avg_rating = sum(t.rating for t in templates) / len(templates) if templates else 0
        
        # Usage by category
        category_usage = {}
        for template in templates:
            category_usage[template.category] = category_usage.get(template.category, 0) + template.usage_count
        
        # Most popular template
        most_popular = max(templates, key=lambda t: t.usage_count) if templates else None
        
        return {
            'total_templates': len(templates),
            'total_usage': total_usage,
            'average_rating': avg_rating,
            'most_popular': most_popular.name if most_popular else None,
            'by_category': category_usage,
            'kawaii_coverage': '100%',
            'workflow_types': list(set(t.workflow_type.value for t in templates))
        }
    
    def suggest_workflow(self, 
                        goal: str,
                        team_size: int,
                        available_time_hours: float) -> List[WorkflowTemplate]:
        """Suggest appropriate workflows based on criteria"""
        candidates = list(self.templates.values())
        
        # Filter by team size
        candidates = [t for t in candidates if t.required_agents <= team_size]
        
        # Filter by time (allow 20% variance)
        time_tolerance = available_time_hours * 0.2
        candidates = [
            t for t in candidates 
            if abs(t.estimated_duration_hours - available_time_hours) <= time_tolerance
        ]
        
        # Score by relevance to goal
        def score_template(template):
            score = 0
            if goal.lower() in template.name.lower():
                score += 10
            if goal.lower() in template.description.lower():
                score += 5
            if any(goal.lower() in tag.lower() for tag in template.tags):
                score += 3
            return score
        
        scored_templates = [(score_template(t), t) for t in candidates]
        scored_templates.sort(key=lambda x: x[0], reverse=True)
        
        return [t for score, t in scored_templates[:5]]  # Top 5 suggestions
    
    def generate_workflow_report(self) -> str:
        """Generate kawaii workflow report"""
        analytics = self.get_workflow_analytics()
        
        report = f"""
🎭 Kawaii Workflow Templates Report ♡
────────────────────────────────────
📋 Total Templates: {analytics['total_templates']}
📊 Total Usage: {analytics['total_usage']} times
⭐ Average Rating: {analytics['average_rating']:.1f}/5.0
🏆 Most Popular: {analytics['most_popular'] or 'N/A'}
💖 Kawaii Coverage: {analytics['kawaii_coverage']}

📂 Categories:
{self._format_category_usage(analytics['by_category'])}

🎯 Ready to launch your next kawaii collaboration! (òωó)
💖 Workflow templates make collaboration magical! ♡
        """
        
        return report
    
    def _format_category_usage(self, category_usage: Dict[str, int]) -> str:
        """Format category usage for report"""
        lines = []
        for category, usage in category_usage.items():
            category_name = WF_CATEGORIES.get(category, category.title())
            lines.append(f"  {category_name}: {usage} uses")
        return '\n'.join(lines) if lines else "  No usage data yet"


# Demo function
def demo_kawaii_workflow_templates():
    """Demonstrate kawaii workflow templates"""
    print("🎀 Kawaii Workflow Templates Demo (òωó)")
    print("=" * 50)
    
    templates = KawaiiWorkflowTemplates()
    
    # Show available templates
    print("\n📋 Available Workflow Templates:")
    for template in templates.list_templates():
        print(f"  🎭 {template.name}")
        print(f"     Category: {WF_CATEGORIES[template.category]}")
        print(f"     Duration: {template.estimated_duration_hours}h | Agents: {template.required_agents}")
        print()
    
    # Show analytics
    print("\n📊 Workflow Analytics:")
    analytics = templates.get_workflow_analytics()
    for key, value in analytics.items():
        print(f"  {key}: {value}")
    
    # Show workflow suggestions
    print("\n💡 Suggested Workflows:")
    suggestions = templates.suggest_workflow("development", 2, 3.0)
    for suggestion in suggestions[:2]:
        print(f"  📋 {suggestion.name} (⭐{suggestion.rating})")
    
    print("\n💖 Demo complete! Ready to launch kawaii workflows! ♡")


if __name__ == "__main__":
    demo_kawaii_workflow_templates()
