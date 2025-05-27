import pandas as pd
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from urllib.parse import urlparse
import logging

@dataclass
class KeywordData:
    keyword: str
    volume: int
    organic_traffic: int
    paid_traffic: int
    average_position: float
    locations: int
    location_name: str
    country: str
    organic_clicks: int
    paid_clicks: int

class CSVKeywordAnalyzer:
    """Analyzes Ahrefs CSV keyword data for competitor analysis"""
    
    def __init__(self, csv_file_path: str):
        self.csv_file_path = csv_file_path
        self.keywords_data: List[KeywordData] = []
        self.logger = logging.getLogger(__name__)
        
    def load_csv_data(self) -> bool:
        """Load and parse CSV data from Ahrefs export"""
        try:
            # Read CSV with proper handling of different encodings
            try:
                df = pd.read_csv(self.csv_file_path, encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(self.csv_file_path, encoding='latin-1')
            
            # Expected columns from Ahrefs export
            expected_columns = [
                'Keyword', 'Volume', 'Organic traffic', 'Paid traffic',
                'Average position', 'Locations', 'Location', 'Country',
                'Organic clicks', 'Paid clicks'
            ]
            
            # Check if required columns exist
            missing_columns = [col for col in expected_columns if col not in df.columns]
            if missing_columns:
                self.logger.warning(f"Missing columns: {missing_columns}")
                # Try alternative column names
                column_mapping = {
                    'Keyword': ['keyword', 'Keyword'],
                    'Volume': ['volume', 'Volume', 'Search Volume'],
                    'Organic traffic': ['organic_traffic', 'Organic traffic', 'Traffic'],
                    'Paid traffic': ['paid_traffic', 'Paid traffic'],
                    'Average position': ['average_position', 'Average position', 'Position'],
                    'Locations': ['locations', 'Locations'],
                    'Location': ['location', 'Location'],
                    'Country': ['country', 'Country'],
                    'Organic clicks': ['organic_clicks', 'Organic clicks'],
                    'Paid clicks': ['paid_clicks', 'Paid clicks']
                }
                
                # Map columns to standardized names
                for standard_name, alternatives in column_mapping.items():
                    for alt in alternatives:
                        if alt in df.columns:
                            if alt != standard_name:
                                df = df.rename(columns={alt: standard_name})
                            break
            
            # Parse data into KeywordData objects
            for _, row in df.iterrows():
                try:
                    keyword_data = KeywordData(
                        keyword=str(row.get('Keyword', '')),
                        volume=int(row.get('Volume', 0)) if pd.notna(row.get('Volume', 0)) else 0,
                        organic_traffic=int(row.get('Organic traffic', 0)) if pd.notna(row.get('Organic traffic', 0)) else 0,
                        paid_traffic=int(row.get('Paid traffic', 0)) if pd.notna(row.get('Paid traffic', 0)) else 0,
                        average_position=float(row.get('Average position', 0)) if pd.notna(row.get('Average position', 0)) else 0,
                        locations=int(row.get('Locations', 0)) if pd.notna(row.get('Locations', 0)) else 0,
                        location_name=str(row.get('Location', '')),
                        country=str(row.get('Country', '')),
                        organic_clicks=int(row.get('Organic clicks', 0)) if pd.notna(row.get('Organic clicks', 0)) else 0,
                        paid_clicks=int(row.get('Paid clicks', 0)) if pd.notna(row.get('Paid clicks', 0)) else 0,
                    )
                    self.keywords_data.append(keyword_data)
                except Exception as e:
                    self.logger.warning(f"Error processing row: {e}")
                    continue
            
            self.logger.info(f"Loaded {len(self.keywords_data)} keywords from CSV")
            return True
            
        except Exception as e:
            self.logger.error(f"Error loading CSV data: {e}")
            return False
    
    def get_top_keywords(self, limit: int = 50, sort_by: str = 'volume') -> List[KeywordData]:
        """Get top keywords sorted by specified metric"""
        if not self.keywords_data:
            return []
        
        if sort_by == 'volume':
            return sorted(self.keywords_data, key=lambda x: x.volume, reverse=True)[:limit]
        elif sort_by == 'traffic':
            return sorted(self.keywords_data, key=lambda x: x.organic_traffic, reverse=True)[:limit]
        elif sort_by == 'position':
            return sorted(self.keywords_data, key=lambda x: x.average_position)[:limit]
        else:
            return self.keywords_data[:limit]
    
    def get_keyword_gaps(self, competitor_url: str, my_url: str) -> Dict:
        """Identify keyword gaps and opportunities"""
        # This will be enhanced with actual webpage analysis
        gaps = {
            'high_volume_opportunities': [],
            'low_competition_keywords': [],
            'position_improvement_targets': [],
            'content_gaps': []
        }
        
        # High volume opportunities (volume > 1000, position > 10)
        for keyword in self.keywords_data:
            if keyword.volume > 1000 and keyword.average_position > 10:
                gaps['high_volume_opportunities'].append({
                    'keyword': keyword.keyword,
                    'volume': keyword.volume,
                    'current_position': keyword.average_position,
                    'traffic_potential': keyword.organic_traffic
                })
        
        # Low competition keywords (volume > 100, position > 20)
        for keyword in self.keywords_data:
            if keyword.volume > 100 and keyword.average_position > 20:
                gaps['low_competition_keywords'].append({
                    'keyword': keyword.keyword,
                    'volume': keyword.volume,
                    'position': keyword.average_position
                })
        
        # Position improvement targets (currently ranking 4-10)
        for keyword in self.keywords_data:
            if 4 <= keyword.average_position <= 10:
                gaps['position_improvement_targets'].append({
                    'keyword': keyword.keyword,
                    'volume': keyword.volume,
                    'current_position': keyword.average_position,
                    'improvement_potential': max(0, keyword.organic_traffic * (1 - keyword.average_position/10))
                })
        
        return gaps
    
    def generate_content_suggestions(self, target_keywords: List[str]) -> Dict:
        """Generate content optimization suggestions based on keywords"""
        suggestions = {
            'primary_keywords': [],
            'secondary_keywords': [],
            'long_tail_opportunities': [],
            'content_themes': []
        }
        
        # Find keywords in our data that match target keywords
        for target in target_keywords:
            matching_keywords = [
                kw for kw in self.keywords_data 
                if target.lower() in kw.keyword.lower()
            ]
            
            if matching_keywords:
                # Sort by volume and categorize
                matching_keywords.sort(key=lambda x: x.volume, reverse=True)
                
                for i, kw in enumerate(matching_keywords[:10]):
                    if i < 3:  # Top 3 as primary
                        suggestions['primary_keywords'].append({
                            'keyword': kw.keyword,
                            'volume': kw.volume,
                            'competition_position': kw.average_position
                        })
                    elif len(kw.keyword.split()) <= 3:  # Short keywords as secondary
                        suggestions['secondary_keywords'].append({
                            'keyword': kw.keyword,
                            'volume': kw.volume
                        })
                    else:  # Long keywords as long-tail
                        suggestions['long_tail_opportunities'].append({
                            'keyword': kw.keyword,
                            'volume': kw.volume
                        })
        
        return suggestions
    
    def export_analysis(self, output_file: str) -> bool:
        """Export analysis results to JSON"""
        try:
            analysis_data = {
                'total_keywords': len(self.keywords_data),
                'top_keywords': [
                    {
                        'keyword': kw.keyword,
                        'volume': kw.volume,
                        'traffic': kw.organic_traffic,
                        'position': kw.average_position
                    } for kw in self.get_top_keywords(20)
                ],
                'keyword_gaps': self.get_keyword_gaps('', ''),
                'summary_stats': self.get_summary_stats()
            }
            
            with open(output_file, 'w') as f:
                json.dump(analysis_data, f, indent=2)
            
            return True
        except Exception as e:
            self.logger.error(f"Error exporting analysis: {e}")
            return False
    
    def get_summary_stats(self) -> Dict:
        """Get summary statistics from the keyword data"""
        if not self.keywords_data:
            return {}
        
        volumes = [kw.volume for kw in self.keywords_data]
        traffic = [kw.organic_traffic for kw in self.keywords_data]
        positions = [kw.average_position for kw in self.keywords_data if kw.average_position > 0]
        
        return {
            'total_keywords': len(self.keywords_data),
            'total_volume': sum(volumes),
            'total_traffic': sum(traffic),
            'avg_volume': sum(volumes) / len(volumes) if volumes else 0,
            'avg_traffic': sum(traffic) / len(traffic) if traffic else 0,
            'avg_position': sum(positions) / len(positions) if positions else 0,
            'top_10_positions': len([p for p in positions if p <= 10]),
            'page_1_positions': len([p for p in positions if p <= 10]),
            'page_2_positions': len([p for p in positions if 11 <= p <= 20])
        } 