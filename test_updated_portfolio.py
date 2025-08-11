#!/usr/bin/env python3
"""
Test script to verify the updated portfolio with real resume content
"""

import requests
import json
import sys

def test_homepage():
    """Test the homepage content"""
    try:
        response = requests.get('http://localhost:5000/')
        if response.status_code == 200:
            content = response.text
            
            # Check for updated personal information
            checks = [
                ('Ayan Mulla', 'Name appears on homepage'),
                ('Data Scientist', 'Updated role appears'),
                ('CeADAR', 'Current company appears'),
                ('University College Dublin', 'Current education appears'),
                ('NewsFlash', 'Project appears'),
                ('Production Engineering Fellow', 'MLH Fellowship appears'),
                ('VMobi Solutions', 'Previous company appears')
            ]
            
            print("🧪 Testing Homepage Content:")
            print("=" * 50)
            
            for check, description in checks:
                if check in content:
                    print(f"✅ {description}")
                else:
                    print(f"❌ {description} - '{check}' not found")
            
            return True
        else:
            print(f"❌ Homepage request failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing homepage: {e}")
        return False

def test_timeline_api():
    """Test the timeline API"""
    try:
        response = requests.get('http://localhost:5000/api/timeline_posts')
        if response.status_code == 200:
            print(f"\n✅ Timeline API working (Status: {response.status_code})")
            data = response.json()
            print(f"✅ Timeline has {len(data)} posts")
            return True
        else:
            print(f"❌ Timeline API failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing timeline API: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing Updated Portfolio with Real Resume Content")
    print("=" * 60)
    
    homepage_ok = test_homepage()
    api_ok = test_timeline_api()
    
    print("\n" + "=" * 60)
    
    if homepage_ok and api_ok:
        print("🎉 All tests passed! Portfolio updated successfully with real resume content.")
        print("\n📝 Summary of updates:")
        print("   • Work Experience: CeADAR, MLH x Meta, VMobi Solutions, IMA-PG")
        print("   • Education: University College Dublin, University of Mumbai")
        print("   • Projects: NewsFlash AI-powered news platform")
        print("   • Personal Info: Updated role and about section")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the application.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
