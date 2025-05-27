import json
import logging
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse
from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup
import re

# Import the existing SEO analyzer
from pyseoanalyzer import analyze

@dataclass
class CompetitorInsight:
    keyword: str
    competitor_position: int
    my_position: Optional[int]
    volume: int
    gap_score: float
    opportunity_type: str

class CompetitorAnalyzer:
    """Compare SEO performance between competitor and your website"""
    
    def __init__(self, keyword_analyzer=None):
        self.keyword_analyzer = keyword_analyzer
        self.logger = logging.getLogger(__name__)
    
    def analyze_competitor_vs_my_site(self, competitor_url: str, my_url: str) -> Dict:
        """Comprehensive comparison between competitor and your site"""
        
        results = {
            'competitor_analysis': {},
            'my_site_analysis': {},
            'comparison': {},
            'recommendations': []
        }
        
        try:
            # Analyze competitor site using the existing SEO analyzer
            self.logger.info(f"Analyzing competitor site: {competitor_url}")
            competitor_analysis = analyze(competitor_url, follow_links=False, analyze_headings=True, analyze_extra_tags=True)
            results['competitor_analysis'] = competitor_analysis
            
            # Analyze my site using the existing SEO analyzer  
            self.logger.info(f"Analyzing your site: {my_url}")
            my_analysis = analyze(my_url, follow_links=False, analyze_headings=True, analyze_extra_tags=True)
            results['my_site_analysis'] = my_analysis
            
            # Perform comparison
            results['comparison'] = self._compare_sites(competitor_analysis, my_analysis)
            
            # Generate keyword-based insights if keyword data is available
            if self.keyword_analyzer and hasattr(self.keyword_analyzer, 'keywords_data'):
                results['keyword_insights'] = self._analyze_keyword_gaps(competitor_url, my_url)
            
            # Generate recommendations
            results['recommendations'] = self._generate_recommendations(results['comparison'])
            
        except Exception as e:
            self.logger.error(f"Error in competitor analysis: {e}")
            results['error'] = str(e)
        
        return results
    
    def _compare_sites(self, competitor_data: Dict, my_data: Dict) -> Dict:
        """Compare technical SEO aspects between sites"""
        
        comparison = {
            'page_analysis': {},
            'content_analysis': {},
            'technical_seo': {},
            'advantages': [],
            'disadvantages': []
        }
        
        # Page-level comparison
        if 'page' in competitor_data and 'page' in my_data:
            comp_page = competitor_data['page']
            my_page = my_data['page']
            
            comparison['page_analysis'] = {
                'title_comparison': {
                    'competitor_title': comp_page.get('title', ''),
                    'my_title': my_page.get('title', ''),
                    'competitor_title_length': len(comp_page.get('title', '')),
                    'my_title_length': len(my_page.get('title', '')),
                },
                'meta_description_comparison': {
                    'competitor_desc': comp_page.get('description', ''),
                    'my_desc': my_page.get('description', ''),
                    'competitor_desc_length': len(comp_page.get('description', '')),
                    'my_desc_length': len(my_page.get('description', '')),
                },
                'headings_comparison': {
                    'competitor_h1_count': len(comp_page.get('h1', [])),
                    'my_h1_count': len(my_page.get('h1', [])),
                    'competitor_h2_count': len(comp_page.get('h2', [])),
                    'my_h2_count': len(my_page.get('h2', [])),
                }
            }
        
        # Content analysis comparison
        if 'words' in competitor_data and 'words' in my_data:
            comp_words = competitor_data['words']
            my_words = my_data['words']
            
            comparison['content_analysis'] = {
                'word_count_comparison': {
                    'competitor_word_count': comp_words.get('count', 0),
                    'my_word_count': my_words.get('count', 0),
                    'word_count_gap': comp_words.get('count', 0) - my_words.get('count', 0)
                },
                'keyword_density_comparison': self._compare_keyword_density(comp_words, my_words)
            }
        
        # Technical SEO comparison
        comparison['technical_seo'] = self._compare_technical_seo(competitor_data, my_data)
        
        # Identify advantages and disadvantages
        comparison['advantages'], comparison['disadvantages'] = self._identify_advantages(comparison)
        
        return comparison
    
    def _compare_keyword_density(self, comp_words: Dict, my_words: Dict) -> Dict:
        """Compare keyword density between sites"""
        
        comp_keywords = comp_words.get('keywords', {})
        my_keywords = my_words.get('keywords', {})
        
        # Get top keywords from competitor
        comp_top_keywords = sorted(comp_keywords.items(), key=lambda x: x[1], reverse=True)[:20]
        
        keyword_gaps = []
        for keyword, comp_density in comp_top_keywords:
            my_density = my_keywords.get(keyword, 0)
            gap = comp_density - my_density
            
            if gap > 0:  # Competitor has higher density
                keyword_gaps.append({
                    'keyword': keyword,
                    'competitor_density': comp_density,
                    'my_density': my_density,
                    'gap': gap,
                    'opportunity_score': gap * 10  # Simple scoring
                })
        
        return {
            'keyword_gaps': sorted(keyword_gaps, key=lambda x: x['gap'], reverse=True),
            'total_gaps': len(keyword_gaps),
            'avg_gap': sum(gap['gap'] for gap in keyword_gaps) / len(keyword_gaps) if keyword_gaps else 0
        }
    
    def _compare_technical_seo(self, competitor_data: Dict, my_data: Dict) -> Dict:
        """Compare technical SEO factors"""
        
        technical_comparison = {}
        
        # Compare warnings/errors
        comp_warnings = competitor_data.get('warnings', [])
        my_warnings = my_data.get('warnings', [])
        
        technical_comparison['warnings_comparison'] = {
            'competitor_warnings': len(comp_warnings),
            'my_warnings': len(my_warnings),
            'my_unique_issues': [w for w in my_warnings if w not in comp_warnings],
            'competitor_issues_i_dont_have': [w for w in comp_warnings if w not in my_warnings]
        }
        
        # Compare page structure
        if 'page' in competitor_data and 'page' in my_data:
            comp_page = competitor_data['page']
            my_page = my_data['page']
            
            technical_comparison['structure_comparison'] = {
                'images': {
                    'competitor_images': len(comp_page.get('images_without_alt', [])),
                    'my_images': len(my_page.get('images_without_alt', [])),
                },
                'links': {
                    'competitor_internal_links': len(comp_page.get('links', {}).get('internal', [])),
                    'my_internal_links': len(my_page.get('links', {}).get('internal', [])),
                    'competitor_external_links': len(comp_page.get('links', {}).get('external', [])),
                    'my_external_links': len(my_page.get('links', {}).get('external', [])),
                }
            }
        
        return technical_comparison
    
    def _identify_advantages(self, comparison: Dict) -> Tuple[List[str], List[str]]:
        """Identify competitive advantages and disadvantages"""
        
        advantages = []
        disadvantages = []
        
        # Title optimization
        if 'page_analysis' in comparison:
            title_comp = comparison['page_analysis'].get('title_comparison', {})
            my_title_len = title_comp.get('my_title_length', 0)
            comp_title_len = title_comp.get('competitor_title_length', 0)
            
            if 50 <= my_title_len <= 60 and (comp_title_len < 50 or comp_title_len > 60):
                advantages.append("Your title length is optimally sized (50-60 chars)")
            elif 50 <= comp_title_len <= 60 and (my_title_len < 50 or my_title_len > 60):
                disadvantages.append("Competitor has better title length optimization")
        
        # Content depth
        if 'content_analysis' in comparison:
            content_comp = comparison['content_analysis'].get('word_count_comparison', {})
            word_gap = content_comp.get('word_count_gap', 0)
            
            if word_gap < -200:  # My content is 200+ words longer
                advantages.append("Your content is more comprehensive (longer word count)")
            elif word_gap > 200:  # Competitor content is 200+ words longer
                disadvantages.append("Competitor has more comprehensive content")
        
        # Technical SEO
        if 'technical_seo' in comparison:
            warnings_comp = comparison['technical_seo'].get('warnings_comparison', {})
            my_warnings = warnings_comp.get('my_warnings', 0)
            comp_warnings = warnings_comp.get('competitor_warnings', 0)
            
            if my_warnings < comp_warnings:
                advantages.append("You have fewer technical SEO issues")
            elif my_warnings > comp_warnings:
                disadvantages.append("You have more technical SEO issues than competitor")
        
        return advantages, disadvantages
    
    def _analyze_keyword_gaps(self, competitor_url: str, my_url: str) -> Dict:
        """Analyze keyword gaps using the loaded keyword data"""
        
        if not self.keyword_analyzer or not hasattr(self.keyword_analyzer, 'keywords_data'):
            return {}
        
        # Get keyword gaps from the keyword analyzer
        keyword_gaps = self.keyword_analyzer.get_keyword_gaps(competitor_url, my_url)
        
        # Enhance with additional analysis
        insights = {
            'high_priority_keywords': [],
            'content_gap_analysis': {},
            'quick_wins': []
        }
        
        # Identify high priority keywords (high volume + currently ranking low)
        for kw_data in self.keyword_analyzer.keywords_data:
            if kw_data.volume > 1000 and kw_data.average_position > 15:
                insights['high_priority_keywords'].append({
                    'keyword': kw_data.keyword,
                    'volume': kw_data.volume,
                    'current_position': kw_data.average_position,
                    'traffic_potential': kw_data.organic_traffic,
                    'priority_score': kw_data.volume * (30 - kw_data.average_position) / 30
                })
        
        # Sort by priority score
        insights['high_priority_keywords'].sort(key=lambda x: x['priority_score'], reverse=True)
        
        # Identify quick wins (position 11-20, volume > 500)
        for kw_data in self.keyword_analyzer.keywords_data:
            if 11 <= kw_data.average_position <= 20 and kw_data.volume > 500:
                insights['quick_wins'].append({
                    'keyword': kw_data.keyword,
                    'volume': kw_data.volume,
                    'current_position': kw_data.average_position,
                    'potential_traffic_gain': kw_data.organic_traffic * 2  # Rough estimate for moving to page 1
                })
        
        insights['quick_wins'].sort(key=lambda x: x['potential_traffic_gain'], reverse=True)
        
        return insights
    
    def _generate_recommendations(self, comparison: Dict) -> List[Dict]:
        """Generate actionable SEO recommendations"""
        
        recommendations = []
        
        # Title optimization recommendations
        if 'page_analysis' in comparison:
            title_comp = comparison['page_analysis'].get('title_comparison', {})
            my_title_len = title_comp.get('my_title_length', 0)
            
            if my_title_len < 30:
                recommendations.append({
                    'category': 'Title Optimization',
                    'priority': 'High',
                    'issue': 'Title is too short',
                    'recommendation': 'Expand your title to 50-60 characters to improve click-through rates',
                    'impact': 'High'
                })
            elif my_title_len > 60:
                recommendations.append({
                    'category': 'Title Optimization', 
                    'priority': 'High',
                    'issue': 'Title is too long',
                    'recommendation': 'Shorten your title to under 60 characters to prevent truncation',
                    'impact': 'High'
                })
        
        # Content recommendations
        if 'content_analysis' in comparison:
            content_comp = comparison['content_analysis'].get('word_count_comparison', {})
            word_gap = content_comp.get('word_count_gap', 0)
            
            if word_gap > 300:
                recommendations.append({
                    'category': 'Content Depth',
                    'priority': 'Medium',
                    'issue': 'Content is less comprehensive than competitor',
                    'recommendation': f'Add approximately {word_gap} more words of valuable content',
                    'impact': 'Medium'
                })
            
            # Keyword density recommendations
            keyword_gaps = content_comp.get('keyword_density_comparison', {}).get('keyword_gaps', [])
            if keyword_gaps:
                top_gap = keyword_gaps[0]
                recommendations.append({
                    'category': 'Keyword Optimization',
                    'priority': 'Medium',
                    'issue': f'Low density for important keyword: {top_gap["keyword"]}',
                    'recommendation': f'Increase mentions of "{top_gap["keyword"]}" by {int(top_gap["gap"])} occurrences',
                    'impact': 'Medium'
                })
        
        # Technical SEO recommendations
        if 'technical_seo' in comparison:
            warnings_comp = comparison['technical_seo'].get('warnings_comparison', {})
            unique_issues = warnings_comp.get('my_unique_issues', [])
            
            for issue in unique_issues[:3]:  # Top 3 issues
                recommendations.append({
                    'category': 'Technical SEO',
                    'priority': 'High',
                    'issue': issue,
                    'recommendation': 'Fix this technical issue to improve SEO performance',
                    'impact': 'High'
                })
        
        return recommendations
    
    def export_comparison_report(self, results: Dict, output_file: str) -> bool:
        """Export comparison results to JSON file"""
        try:
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            return True
        except Exception as e:
            self.logger.error(f"Error exporting comparison report: {e}")
            return False 