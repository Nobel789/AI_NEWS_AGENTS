from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, FileWriterTool

load_dotenv()

@CrewBase
class AiNewsAgents():
    """AiNewsAgents crew"""

    @agent
    def news_agent(self) -> Agent:
        return Agent(
            role='{topic} News Retriever',
            goal='Uncover cutting-edge developments in {topic}',
            backstory="You're a seasoned researcher with a knack for uncovering the latest developments in {topic}. Known for your ability to find the most relevant information and present it in a clear and concise manner.",
            tools=[SerperDevTool()],
            verbose=True
        )

    @agent
    def webscrapper_agent(self) -> Agent:
        return Agent(
            role='News Website Scraper',
            goal='Scrape the website for latest news and information',
            backstory="You're a skilled scraper with a knack for extracting the latest developments in {topic}. Known for your ability to find the most relevant information and present it in a clear and concise manner.",
            tools=[ScrapeWebsiteTool()],
            verbose=True
        )
    
    @agent
    def fact_checker_agent(self) -> Agent:
        return Agent(
            role='Fact-Checking Specialist',
            goal='Verify the credibility and accuracy of news sources and content before summarization',
            backstory=(
                "You're a meticulous fact-checker with expertise in media literacy and source verification. "
                "You have a keen eye for detecting bias, misinformation, and unreliable sources. Your role is "
                "crucial in maintaining the integrity and trustworthiness of the news reporting process. "
                "You analyze domain reputation, check for bias indicators, and provide credibility scores for sources."
            ),
            tools=[],  # Using agent reasoning instead of external tools
            verbose=True
        )
    
    @agent
    def filegenerate_analyst(self) -> Agent:
        return Agent(
            role='News Report Writer & Publisher',
            goal='Create comprehensive, copy-ready news reports that require no further editing',
            backstory=(
                "You're a senior news editor and professional writer specializing in technology journalism. "
                "Your expertise lies in transforming raw information into polished, publication-ready articles "
                "that readers can immediately understand and share. You excel at creating engaging headlines, "
                "structuring complex information clearly, and maintaining journalistic integrity. Every report "
                "you create includes transparent credibility assessments to build reader trust. Your articles "
                "are ready for immediate publication, sharing on social media, or distribution to stakeholders "
                "without any additional editing required."
            ),
            tools=[FileWriterTool()],
            verbose=True
        )

    @task
    def generate_news_task(self) -> Task:
        return Task(
            description='Generate news about AI LLMs.',
            expected_output='A list with 4 websites of the most relevant information about {topic}',
            agent=self.news_agent()
        )

    @task
    def fact_checking_task(self) -> Task:
        return Task(
            description=(
                'Verify the credibility and reliability of sources found by the news agent. '
                'For each source URL, analyze:\n'
                '1. Domain reputation (check if from reputable sources like Reuters, BBC, AP, NYT, etc.)\n'
                '2. Source type (established media, academic, government, blog, etc.)\n'
                '3. Potential bias indicators\n'
                '4. Overall credibility assessment\n'
                'Rate each source on a scale of 0-100 for credibility and provide recommendations.\n'
                'Focus on well-known, established news sources for AI and technology coverage.'
            ),
            expected_output=(
                'A comprehensive fact-checking report including:\n'
                '- Credibility score (0-100) for each source\n'
                '- Domain reputation analysis (high/medium/low)\n'
                '- Source type classification\n'
                '- Bias assessment and red flags\n'
                '- Recommendations for each source (use/cross-reference/avoid)\n'
                '- Final list of approved sources for scraping\n'
                '- Summary of fact-checking methodology used'
            ),
            agent=self.fact_checker_agent()
        )

    @task
    def webscraping_task(self) -> Task:
        return Task(
            description=(
                'Scrape only the verified and credible websites approved by the fact-checking agent. '
                'Focus on sources with high credibility scores and avoid those flagged as unreliable. '
                'Extract comprehensive information while maintaining awareness of any bias indicators noted in the fact-check report.'
            ),
            expected_output='Fully scraped content from verified sources with credibility context and bias awareness',
            agent=self.webscrapper_agent(),
            context=[self.fact_checking_task()],  # Depends on fact-checking results
            output_file='report.md'
        )
    
    @task
    def filegenerate_task(self) -> Task:
        return Task(
            description=(
                'Create a comprehensive, publication-ready news report that synthesizes all information '
                'from verified sources into a polished article. Follow this exact structure:\n\n'
                '**ARTICLE FORMAT:**\n'
                '1. Compelling headline (clear and informative)\n'
                '2. Executive Summary (150 words max - key highlights)\n'
                '3. Main Content Sections:\n'
                '   - Key Developments (most important news)\n'
                '   - Industry Impact & Analysis\n'
                '   - Expert Insights & Quotes\n'
                '   - Future Outlook & Trends\n'
                '4. Professional conclusion\n\n'
                '**CREDIBILITY SECTION (SEPARATE):**\n'
                'Add a dedicated "Source Credibility Assessment" section that includes:\n'
                '- Credibility scores for each source (X/100)\n'
                '- Domain reputation classification (High/Medium/Low)\n'
                '- Source diversity analysis\n'
                '- Fact-checking methodology summary\n'
                '- Any bias indicators or red flags noted\n\n'
                '**STYLE REQUIREMENTS:**\n'
                '- Professional journalistic tone\n'
                '- Clear, engaging writing\n'
                '- Proper citations and attributions\n'
                '- Ready for immediate copy/paste use\n'
                '- No technical jargon without explanation'
            ),
            expected_output=(
                'A complete, professional news report saved as markdown file with:\n\n'
                '✓ Professional headline and structure\n'
                '✓ 1000-1500 word comprehensive article\n'
                '✓ Clear sections with engaging content\n'
                '✓ Separate credibility assessment paragraph\n'
                '✓ Source transparency and fact-checking notes\n'
                '✓ Professional formatting and citations\n'
                '✓ Ready for publication/sharing\n\n'
                'File: news/{date}_comprehensive_ai_news_report.md'
            ),
            agent=self.filegenerate_analyst(),
            context=[self.fact_checking_task(), self.webscraping_task()],
            output_file='news/comprehensive_ai_news_report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the AiNewsAgents crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
