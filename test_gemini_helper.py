"""Test cases for Gemini Helper API Key Validation"""
import sys
import os

# Add project paths
root_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, root_path)

from gemini_helper import GeminiQMDGHelper


def test_validate_leaked_key():
    """Test that leaked keys are properly detected"""
    # Note: This would need a real leaked key to test properly
    # For safety, we'll just test the format validation
    helper = GeminiQMDGHelper("")
    
    # Test invalid format
    is_valid, status, msg = helper.validate_api_key("invalid_key")
    assert is_valid == False, "Invalid key should fail validation"
    assert status == "INVALID_FORMAT", f"Expected INVALID_FORMAT, got {status}"
    print("✅ Test invalid format: PASSED")


def test_validate_empty_key():
    """Test that empty keys are rejected"""
    helper = GeminiQMDGHelper("")
    
    is_valid, status, msg = helper.validate_api_key("")
    assert is_valid == False, "Empty key should fail"
    assert status == "INVALID_FORMAT", f"Expected INVALID_FORMAT, got {status}"
    print("✅ Test empty key: PASSED")


def test_key_format_validation():
    """Test key format checks"""
    helper = GeminiQMDGHelper("")
    
    # Test wrong prefix
    is_valid, status, msg = helper.validate_api_key("WRONG" + "X" * 35)
    assert is_valid == False, "Wrong prefix should fail"
    assert status == "INVALID_FORMAT"
    print("✅ Test wrong prefix: PASSED")
    
    # Test wrong length
    is_valid, status, msg = helper.validate_api_key("AIza" + "X" * 30)  # Too short
    assert is_valid == False, "Wrong length should fail"
    assert status == "INVALID_FORMAT"
    print("✅ Test wrong length: PASSED")


def test_test_connection_no_key():
    """Test that test_connection handles missing keys"""
    helper = GeminiQMDGHelper("")
    
    result = helper.test_connection()
    success = result[0]
    status = result[2] if len(result) >= 3 else "UNKNOWN"
    
    assert success == False, "No key should fail connection"
    assert status == "NO_KEY", f"Expected NO_KEY, got {status}"
    print("✅ Test no key connection: PASSED")


if __name__ == "__main__":
    print("\n🧪 Running Gemini Helper API Key Validation Tests...\n")
    
    try:
        test_validate_empty_key()
        test_key_format_validation()
        test_validate_leaked_key()
        test_test_connection_no_key()
        
        print("\n✅ ALL TESTS PASSED!\n")
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n🛑 ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
