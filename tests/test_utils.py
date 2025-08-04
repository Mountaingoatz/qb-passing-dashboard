"""
Unit tests for NFL QB dashboard utility functions.
"""

import pytest
import pandas as pd
import numpy as np
from scenes.utils.qb_helpers import bin_direction, bin_depth, bin_playclock

class TestQBHelpers:
    """Test cases for QB helper functions."""
    
    def test_bin_direction(self):
        """Test direction binning function."""
        # Test basic directions
        assert bin_direction('N') == 'N'
        assert bin_direction('NE') == 'NE'
        assert bin_direction('E') == 'E'
        assert bin_direction('SE') == 'SE'
        assert bin_direction('S') == 'S'
        assert bin_direction('SW') == 'SW'
        assert bin_direction('W') == 'W'
        assert bin_direction('NW') == 'NW'
        
        # Test case insensitivity
        assert bin_direction('n') == 'N'
        assert bin_direction('ne') == 'NE'
        
        # Test full names
        assert bin_direction('NORTH') == 'N'
        assert bin_direction('NORTHEAST') == 'NE'
        
        # Test invalid/unknown directions
        assert bin_direction('INVALID') == 'E'  # Default
        assert bin_direction(None) == 'E'  # Default
        assert bin_direction('') == 'E'  # Default
    
    def test_bin_depth(self):
        """Test depth binning function."""
        # Test short passes (0-10 yards)
        assert bin_depth(0) == '0-10 yd'
        assert bin_depth(5) == '0-10 yd'
        assert bin_depth(10) == '0-10 yd'
        
        # Test intermediate passes (10-20 yards)
        assert bin_depth(11) == '10-20 yd'
        assert bin_depth(15) == '10-20 yd'
        assert bin_depth(20) == '10-20 yd'
        
        # Test deep passes (20+ yards)
        assert bin_depth(21) == '20+ yd'
        assert bin_depth(30) == '20+ yd'
        assert bin_depth(50) == '20+ yd'
        
        # Test edge cases
        assert bin_depth(None) == '0-10 yd'  # Default
        assert bin_depth(np.nan) == '0-10 yd'  # Default
    
    def test_bin_playclock(self):
        """Test play clock binning function."""
        # Test different time ranges
        assert bin_playclock(0) == '0-5s'
        assert bin_playclock(5) == '0-5s'
        
        assert bin_playclock(6) == '5-10s'
        assert bin_playclock(10) == '5-10s'
        
        assert bin_playclock(11) == '10-15s'
        assert bin_playclock(15) == '10-15s'
        
        assert bin_playclock(16) == '15-20s'
        assert bin_playclock(20) == '15-20s'
        
        assert bin_playclock(21) == '20-25s'
        assert bin_playclock(25) == '20-25s'
        
        assert bin_playclock(26) == '25-30s'
        assert bin_playclock(30) == '25-30s'
        
        assert bin_playclock(31) == '30-35s'
        assert bin_playclock(35) == '30-35s'
        
        assert bin_playclock(36) == '35-40s'
        assert bin_playclock(40) == '35-40s'
        
        # Test edge cases
        assert bin_playclock(None) == '15-20s'  # Default
        assert bin_playclock(-1) == '15-20s'  # Default
        assert bin_playclock(50) == '35-40s'  # Max range

if __name__ == "__main__":
    pytest.main([__file__]) 