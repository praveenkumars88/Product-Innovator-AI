"""
File Output Utilities
Saves agent outputs to organized files
"""
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import json
import structlog

logger = structlog.get_logger(__name__)


def save_outputs_to_files(results: Dict[str, Any], session_id: str, output_dir: Optional[Path] = None) -> Dict[str, str]:
    """
    Save all outputs from the orchestrator to organized files
    
    Args:
        results: The results dictionary from orchestrator.process()
        session_id: Session ID for organizing files
        output_dir: Optional output directory (defaults to outputs/ in project root)
        
    Returns:
        Dictionary mapping output type to file path
    """
    # Determine output directory
    if output_dir is None:
        project_root = Path(__file__).parent.parent.parent
        output_dir = project_root / 'outputs'
    else:
        output_dir = Path(output_dir)
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True)
    
    # Create session-specific subdirectory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_dir = output_dir / f"{session_id}_{timestamp}"
    session_dir.mkdir(exist_ok=True)
    
    saved_files = {}
    intent = results.get("intent", "unknown")
    domain = results.get("domain", "general")
    
    # Sanitize domain and intent for filenames
    safe_domain = "".join(c for c in domain if c.isalnum() or c in (' ', '-', '_')).strip().replace(' ', '_')[:50]
    safe_intent = intent.replace('_', '-')
    
    try:
        # Save concept paper (for feature extensions)
        if "concept_paper" in results:
            concept = results.get("concept_paper", {})
            concept_text = concept.get("full_text", "")
            if concept_text:
                concept_file = session_dir / f"concept_paper_{safe_domain}.md"
                with open(concept_file, 'w', encoding='utf-8') as f:
                    f.write(concept_text)
                saved_files["concept_paper"] = str(concept_file)
                logger.info("Saved concept paper", file=str(concept_file))
        
        # Save pitch deck (for new app ideas and feature extensions)
        if "pitch" in results:
            pitch = results.get("pitch", {})
            pitch_text = pitch.get("full_text", "")
            if pitch_text:
                # Save as Marp format (can be converted to visual slides)
                pitch_file = session_dir / f"pitch_deck_{safe_domain}.md"
                with open(pitch_file, 'w', encoding='utf-8') as f:
                    f.write(pitch_text)
                saved_files["pitch"] = str(pitch_file)
                logger.info("Saved pitch deck", file=str(pitch_file))
                
                # Create a guide for converting to visual slides
                pitch_guide_file = session_dir / f"pitch_deck_guide_{safe_domain}.md"
                with open(pitch_guide_file, 'w', encoding='utf-8') as f:
                    f.write("# Pitch Deck Conversion Guide\n\n")
                    f.write("## Overview\n\n")
                    f.write(f"The pitch deck is saved in Marp format: `pitch_deck_{safe_domain}.md`\n\n")
                    f.write("## Converting to Visual Slides\n\n")
                    f.write("### Option 1: Marp (Recommended)\n")
                    f.write("1. Install Marp CLI: `npm install -g @marp-team/marp-cli`\n")
                    f.write(f"2. Convert to PDF: `marp pitch_deck_{safe_domain}.md -o pitch_deck_{safe_domain}.pdf`\n")
                    f.write(f"3. Convert to HTML: `marp pitch_deck_{safe_domain}.md -o pitch_deck_{safe_domain}.html`\n")
                    f.write(f"4. Convert to PowerPoint: `marp pitch_deck_{safe_domain}.md -o pitch_deck_{safe_domain}.pptx`\n\n")
                    f.write("### Option 2: Online Marp Editor\n")
                    f.write("1. Go to https://marp.app/\n")
                    f.write(f"2. Copy content from `pitch_deck_{safe_domain}.md`\n")
                    f.write("3. Export as PDF, PowerPoint, or HTML\n\n")
                    f.write("### Option 3: VS Code Extension\n")
                    f.write("1. Install 'Marp for VS Code' extension\n")
                    f.write(f"2. Open `pitch_deck_{safe_domain}.md`\n")
                    f.write("3. Use preview and export features\n\n")
                    f.write("### Option 4: Manual Conversion\n")
                    f.write("Copy each slide section to PowerPoint, Google Slides, or Keynote manually.\n\n")
                saved_files["pitch_guide"] = str(pitch_guide_file)
        
        # Save wireframes (both text and detailed versions)
        if "wireframes" in results:
            wireframes = results.get("wireframes", {})
            wireframe_text = ""
            wireframe_detailed = ""
            
            # Extract wireframe data - structure is wireframes.wireframes dict
            if isinstance(wireframes, dict):
                if "wireframes" in wireframes:
                    wireframes_dict = wireframes.get("wireframes", {})
                    # wireframes_dict is a dict with screen names as keys
                    for screen_name, wf_data in wireframes_dict.items():
                        if isinstance(wf_data, dict):
                            # Simple wireframe version
                            wireframe_text += f"## {screen_name}\n\n"
                            simple_wf = wf_data.get("wireframe", "")
                            if simple_wf:
                                wireframe_text += f"{simple_wf}\n\n"
                            
                            # Detailed wireframe version (from raw_analysis)
                            wireframe_detailed += f"# {screen_name}\n\n"
                            raw_analysis = wf_data.get("raw_analysis", "")
                            if raw_analysis:
                                wireframe_detailed += f"{raw_analysis}\n\n"
                            
                            # Add elements if available
                            elements = wf_data.get("elements", [])
                            if elements:
                                wireframe_detailed += f"## UI Elements\n\n"
                                for elem in elements:
                                    wireframe_detailed += f"- {elem}\n"
                                wireframe_detailed += "\n"
                        else:
                            wireframe_text += f"## {screen_name}\n\n{str(wf_data)}\n\n"
                else:
                    # Fallback: treat wireframes as a list or other structure
                    wireframe_text = str(wireframes)
                    wireframe_detailed = str(wireframes)
            else:
                wireframe_text = str(wireframes)
                wireframe_detailed = str(wireframes)
            
            # Save simple text version
            if wireframe_text:
                wireframe_file = session_dir / f"wireframes_{safe_domain}.txt"
                with open(wireframe_file, 'w', encoding='utf-8') as f:
                    f.write(wireframe_text)
                saved_files["wireframes"] = str(wireframe_file)
                logger.info("Saved wireframes (text)", file=str(wireframe_file))
            
            # Save detailed version with ASCII art
            if wireframe_detailed:
                wireframe_detailed_file = session_dir / f"wireframes_detailed_{safe_domain}.md"
                with open(wireframe_detailed_file, 'w', encoding='utf-8') as f:
                    f.write(wireframe_detailed)
                saved_files["wireframes_detailed"] = str(wireframe_detailed_file)
                logger.info("Saved wireframes (detailed)", file=str(wireframe_detailed_file))
            
            # Generate image wireframes description file
            # This file contains instructions for generating visual wireframes
            wireframe_image_guide = session_dir / f"wireframes_image_guide_{safe_domain}.md"
            with open(wireframe_image_guide, 'w', encoding='utf-8') as f:
                f.write("# Wireframe Image Generation Guide\n\n")
                f.write("## Overview\n\n")
                f.write("This guide explains how to convert the ASCII wireframes into visual wireframe images.\n\n")
                f.write("## Available Formats\n\n")
                f.write("### 1. Text Wireframes\n")
                f.write(f"- File: `wireframes_{safe_domain}.txt`\n")
                f.write("- Simple text representation of wireframes\n\n")
                f.write("### 2. Detailed ASCII Wireframes\n")
                f.write(f"- File: `wireframes_detailed_{safe_domain}.md`\n")
                f.write("- Detailed ASCII art wireframes with full layout\n\n")
                f.write("## Image Generation Options\n\n")
                f.write("### Option 1: Mermaid Diagrams\n")
                f.write("Convert ASCII wireframes to Mermaid flowcharts:\n")
                f.write("```mermaid\n")
                f.write("graph TD\n")
                f.write("    A[Screen Header] --> B[Content Area]\n")
                f.write("    B --> C[Footer]\n")
                f.write("```\n\n")
                f.write("### Option 2: AI Image Generation\n")
                f.write("Use AI tools like:\n")
                f.write("- DALL-E / Midjourney: Describe the wireframe layout\n")
                f.write("- Stable Diffusion: Use ASCII wireframe as prompt\n")
                f.write("- ChatGPT / Claude: Request visual wireframe generation\n\n")
                f.write("### Option 3: Design Tools\n")
                f.write("Import ASCII wireframes into:\n")
                f.write("- Figma: Create frames based on ASCII layout\n")
                f.write("- Excalidraw: Draw wireframes manually\n")
                f.write("- Balsamiq: Use wireframe templates\n\n")
                f.write("### Option 4: Code-Based Generation\n")
                f.write("Use libraries like:\n")
                f.write("- Python: `matplotlib`, `PIL` for programmatic wireframes\n")
                f.write("- JavaScript: `D3.js`, `React` for interactive wireframes\n\n")
                f.write("## Next Steps\n\n")
                f.write("1. Review the detailed ASCII wireframes in `wireframes_detailed_{safe_domain}.md`\n")
                f.write("2. Choose your preferred image generation method\n")
                f.write("3. Generate visual wireframes based on the ASCII layouts\n")
                f.write("4. Save images in formats like PNG, SVG, or PDF\n\n")
            saved_files["wireframes_image_guide"] = str(wireframe_image_guide)
        
        # Save architecture document (only for new app ideas, not feature extensions)
        # Skip architecture for feature extensions as they integrate with existing architecture
        intent = results.get("intent", "")
        if "architecture" in results and intent != "feature_extension":
            architecture = results.get("architecture", {})
            arch_text = ""
            
            if isinstance(architecture, dict):
                arch_text = f"# Architecture Design\n\n"
                
                # Use raw_architecture if available (contains full detailed spec)
                if architecture.get("raw_architecture"):
                    arch_text += f"{architecture.get('raw_architecture')}\n\n"
                else:
                    arch_text += f"## Overview\n\n{architecture.get('overview', architecture.get('description', ''))}\n\n"
                    
                    if "components" in architecture:
                        arch_text += "## Components\n\n"
                        for comp in architecture.get("components", []):
                            arch_text += f"- {comp}\n"
                        arch_text += "\n"
                    
                    if "tech_stack" in architecture:
                        arch_text += "## Technology Stack\n\n"
                        for tech in architecture.get("tech_stack", []):
                            arch_text += f"- {tech}\n"
                        arch_text += "\n"
                    
                    if "architecture_diagram" in architecture:
                        arch_text += f"## Architecture Diagram\n\n```\n{architecture.get('architecture_diagram')}\n```\n\n"
                    
                    # Add any other fields
                    for key, value in architecture.items():
                        if key not in ["overview", "description", "components", "tech_stack", "architecture_diagram", "raw_architecture"]:
                            arch_text += f"## {key.replace('_', ' ').title()}\n\n{value}\n\n"
            else:
                arch_text = str(architecture)
            
            if arch_text:
                arch_file = session_dir / f"architecture_{safe_domain}.md"
                with open(arch_file, 'w', encoding='utf-8') as f:
                    f.write(arch_text)
                saved_files["architecture"] = str(arch_file)
                logger.info("Saved architecture", file=str(arch_file))
        
        # Save feature design (for feature extensions)
        if "feature_design" in results:
            feature = results.get("feature_design", {})
            feature_text = f"# Feature Design\n\n"
            feature_text += f"## Feature Request\n\n{feature.get('feature_request', 'N/A')}\n\n"
            feature_text += f"## Overview\n\n{feature.get('feature_overview', 'N/A')}\n\n"
            
            if "user_stories" in feature:
                feature_text += "## User Stories\n\n"
                for story in feature.get("user_stories", []):
                    feature_text += f"- {story}\n"
                feature_text += "\n"
            
            if "user_journey" in feature:
                feature_text += "## User Journey\n\n"
                journey = feature.get("user_journey", [])
                if isinstance(journey, list):
                    for step in journey:
                        feature_text += f"- {step}\n"
                else:
                    feature_text += f"{journey}\n"
                feature_text += "\n"
            
            if "technical_requirements" in feature:
                feature_text += "## Technical Requirements\n\n"
                for req in feature.get("technical_requirements", []):
                    feature_text += f"- {req}\n"
                feature_text += "\n"
            
            feature_file = session_dir / f"feature_design_{safe_domain}.md"
            with open(feature_file, 'w', encoding='utf-8') as f:
                f.write(feature_text)
            saved_files["feature_design"] = str(feature_file)
            logger.info("Saved feature design", file=str(feature_file))
        
        # Save idea breakdown (for new app ideas)
        if "idea_breakdown" in results:
            idea = results.get("idea_breakdown", {})
            idea_text = f"# Idea Breakdown\n\n"
            idea_text += f"## Problem Statement\n\n{idea.get('problem_statement', 'N/A')}\n\n"
            idea_text += f"## Value Proposition\n\n{idea.get('value_proposition', 'N/A')}\n\n"
            idea_text += f"## Target Audience\n\n{idea.get('target_audience', 'N/A')}\n\n"
            
            if "proposed_features" in idea:
                idea_text += "## Proposed Features\n\n"
                for feature in idea.get("proposed_features", []):
                    idea_text += f"- {feature}\n"
                idea_text += "\n"
            
            idea_file = session_dir / f"idea_breakdown_{safe_domain}.md"
            with open(idea_file, 'w', encoding='utf-8') as f:
                f.write(idea_text)
            saved_files["idea_breakdown"] = str(idea_file)
            logger.info("Saved idea breakdown", file=str(idea_file))
        
        # Save market size analysis
        if "market_size" in results:
            market = results.get("market_size", {})
            market_text = f"# Market Size Analysis\n\n"
            
            if "tam" in market:
                tam = market.get("tam", {})
                market_text += f"## Total Addressable Market (TAM)\n\n"
                market_text += f"Value: ${tam.get('value_usd', 0):,}\n"
                market_text += f"Currency: {tam.get('currency', 'USD')}\n"
                market_text += f"Description: {tam.get('description', '')}\n\n"
            
            if "sam" in market:
                sam = market.get("sam", {})
                market_text += f"## Serviceable Addressable Market (SAM)\n\n"
                market_text += f"Value: ${sam.get('value_usd', 0):,}\n"
                market_text += f"Currency: {sam.get('currency', 'USD')}\n"
                market_text += f"Description: {sam.get('description', '')}\n\n"
            
            if "som" in market:
                som = market.get("som", {})
                market_text += f"## Serviceable Obtainable Market (SOM)\n\n"
                market_text += f"Value: ${som.get('value_usd', 0):,}\n"
                market_text += f"Currency: {som.get('currency', 'USD')}\n"
                market_text += f"Description: {som.get('description', '')}\n\n"
            
            market_file = session_dir / f"market_analysis_{safe_domain}.md"
            with open(market_file, 'w', encoding='utf-8') as f:
                f.write(market_text)
            saved_files["market_size"] = str(market_file)
            logger.info("Saved market analysis", file=str(market_file))
        
        # Save competitor analysis
        if "competitor_analysis" in results:
            competitor = results.get("competitor_analysis", {})
            comp_text = f"# Competitor Analysis\n\n"
            
            # Use raw_analysis if available (contains full detailed analysis)
            if competitor.get("raw_analysis"):
                comp_text += f"{competitor.get('raw_analysis')}\n\n"
            else:
                # Fallback to structured fields
                if "competitors" in competitor:
                    comp_text += "## Competitors\n\n"
                    for comp in competitor.get("competitors", []):
                        if isinstance(comp, dict):
                            comp_text += f"### {comp.get('name', 'Unknown')}\n\n"
                            comp_text += f"{comp.get('description', '')}\n\n"
                        else:
                            comp_text += f"- {comp}\n"
                    comp_text += "\n"
                
                if "top_competitors" in competitor:
                    comp_text += "## Top Competitors\n\n"
                    for comp in competitor.get("top_competitors", []):
                        if isinstance(comp, dict):
                            comp_text += f"### {comp.get('name', 'Unknown')}\n\n"
                            comp_text += f"{comp.get('description', '')}\n\n"
                        else:
                            comp_text += f"- {comp}\n"
                    comp_text += "\n"
                
                if "differentiation" in competitor:
                    comp_text += "## Differentiation\n\n"
                    comp_text += f"{competitor.get('differentiation', '')}\n\n"
                
                if "differentiation_opportunities" in competitor:
                    comp_text += "## Differentiation Opportunities\n\n"
                    for opp in competitor.get("differentiation_opportunities", []):
                        comp_text += f"- {opp}\n"
                    comp_text += "\n"
                
                if "market_gaps" in competitor:
                    comp_text += "## Market Gaps\n\n"
                    for gap in competitor.get("market_gaps", []):
                        comp_text += f"- {gap}\n"
                    comp_text += "\n"
            
            comp_file = session_dir / f"competitor_analysis_{safe_domain}.md"
            with open(comp_file, 'w', encoding='utf-8') as f:
                f.write(comp_text)
            saved_files["competitor_analysis"] = str(comp_file)
            logger.info("Saved competitor analysis", file=str(comp_file))
        
        # Save domain analysis
        if "domain_analysis" in results:
            domain_analysis = results.get("domain_analysis", {})
            domain_text = f"# Domain Analysis\n\n"
            domain_text += f"Domain: {safe_domain or 'N/A'}\n\n"
            
            if isinstance(domain_analysis, dict):
                for key, value in domain_analysis.items():
                    domain_text += f"## {key.replace('_', ' ').title()}\n\n"
                    if isinstance(value, list):
                        for item in value:
                            domain_text += f"- {item}\n"
                    else:
                        domain_text += f"{value}\n"
                    domain_text += "\n"
            else:
                domain_text += str(domain_analysis)
            
            domain_file = session_dir / f"domain_analysis_{safe_domain}.md"
            with open(domain_file, 'w', encoding='utf-8') as f:
                f.write(domain_text)
            saved_files["domain_analysis"] = str(domain_file)
            logger.info("Saved domain analysis", file=str(domain_file))
        
        # Save complete results as JSON (for reference)
        json_file = session_dir / "complete_results.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, default=str)
        saved_files["complete_results"] = str(json_file)
        
        # Create a README file with summary
        readme_file = session_dir / "README.md"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(f"# MAPIS Output - {session_id}\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"## Summary\n\n")
            f.write(f"- **Intent**: {intent}\n")
            f.write(f"- **Domain**: {domain}\n")
            f.write(f"- **User Input**: {results.get('user_input', 'N/A')}\n\n")
            f.write(f"## Generated Files\n\n")
            for output_type, file_path in saved_files.items():
                if output_type != "complete_results":
                    f.write(f"- **{output_type.replace('_', ' ').title()}**: `{Path(file_path).name}`\n")
            f.write(f"\n## Complete Results\n\n")
            f.write(f"Full JSON results available in `complete_results.json`\n")
        saved_files["readme"] = str(readme_file)
        
        logger.info("Saved all outputs to files", output_dir=str(session_dir), files=list(saved_files.keys()))
        
    except Exception as e:
        logger.error("Error saving outputs to files", error=str(e))
        import traceback
        logger.debug("Traceback", traceback=traceback.format_exc())
    
    return saved_files

