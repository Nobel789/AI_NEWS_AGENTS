# How to Check if Your Enhanced AI News Agents is Working

## Quick Verification Methods

### 1. 📋 File Structure Check
Verify these files exist in your project:
```
src/ai_news_agents/tools/fact_check_tool.py  ✓
src/ai_news_agents/crew.py (enhanced)        ✓
FACT_CHECKING_ENHANCEMENT.md                 ✓
verify_system.py                             ✓
```

### 2. 🧪 Run Verification Script
```bash
uv run python verify_system.py
```
This tests:
- Tool imports
- Basic fact-checking functionality  
- Crew configuration
- Agent count verification

### 3. 🚀 Run the Full System
```bash
uv run crewai run
```
Look for these indicators:
- **4 agents** should be listed (including Fact-Checking Specialist)
- **4 tasks** should execute in sequence
- You should see fact-checking analysis in the output

### 4. 🔍 Check Output Quality
After running, your reports should include:
- Source credibility scores (0-100)
- Domain reputation analysis
- Bias indicators
- Fact-checking methodology notes

### 5. 📊 Expected Workflow
You should see this sequence:
1. **News Agent** → Finds sources
2. **Fact-Checking Agent** → Analyzes credibility
3. **Web Scrapper** → Scrapes verified sources only
4. **File Generator** → Creates enhanced report

## What to Look For

### ✅ Success Indicators
- All 4 agents start successfully
- Fact-checking analysis appears in logs
- Output includes credibility information
- No import or tool errors

### ❌ Potential Issues
- Import errors → Check dependencies with `uv sync`
- Missing agent → Check crew.py configuration
- Tool errors → Verify tool implementation

## Manual Testing

### Test Individual Components
```python
# Test fact-checking tool
from src.ai_news_agents.tools.fact_check_tool import FactCheckTool
tool = FactCheckTool()
result = tool._run("https://reuters.com", "")
print(result['credibility_score'])  # Should be high (70+)

# Test with questionable source
result2 = tool._run("https://fakenews.blog", "")
print(result2['credibility_score'])  # Should be low (30-)
```

### Check Agent Configuration
```python
from src.ai_news_agents.crew import AiNewsAgents
crew = AiNewsAgents()
print(f"Agents: {len(crew.agents)}")  # Should be 4
print(f"Tasks: {len(crew.tasks)}")    # Should be 4
```

## Troubleshooting

### Common Issues & Solutions

1. **Import Errors**
   ```bash
   uv sync  # Reinstall dependencies
   ```

2. **Tool Not Found**
   - Check `tools/__init__.py` includes new imports
   - Verify file paths are correct

3. **Agent Missing**
   - Check `crew.py` has `fact_checker_agent()` method
   - Verify agent is included in workflow

4. **No Fact-Checking Output**
   - Check task dependencies in `crew.py`
   - Verify fact-checking task is properly configured

## Expected Performance

### Credibility Scores
- **Reuters, BBC, AP News**: 70-90 points
- **Unknown domains**: 40-60 points  
- **Suspicious domains**: 0-30 points

### Bias Detection
- Should flag emotional language
- Detect conspiracy indicators
- Identify lack of source attribution

### Source Validation
- Analyze source diversity
- Check consensus levels
- Provide usage recommendations

Your enhanced system is working correctly if you see credibility analysis, bias detection, and transparent source reporting in your final output!
