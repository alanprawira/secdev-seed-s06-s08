#!/bin/bash
# S06 Demonstrable Vulnerability One-Liners
# For container testing

echo "================================================"
echo "S06 - SECURITY TEST ONE-LINERS"
echo "================================================"

wait_for_app() {
    echo "Waiting for app to be ready..."
    until curl -s http://localhost:8000/ > /dev/null; do
        sleep 2
    done
    echo "App is ready!"
}

run_tests() {
    echo ""
    echo "1. TESTING SQL INJECTION IN LOGIN (Should FAIL):"
    curl -X POST "http://localhost:8000/login" \
      -H "Content-Type: application/json" \
      -d '{"username":"admin'\''-- ","password":"anything"}' \
      -w " -> HTTP Status: %{http_code}\n" \
      -s

    echo ""
    echo "2. TESTING SQL INJECTION IN SEARCH (Should return LIMITED results):"
    result=$(curl -s "http://localhost:8000/search?q=test%27%20OR%20%271%27%3D%271%27--")
    item_count=$(echo "$result" | python3 -c "import sys, json; print(len(json.load(sys.stdin)['items']))")
    echo "Items returned: $item_count"

    echo ""
    echo "3. TESTING XSS PROTECTION (Script tags should be ESCAPED):"
    xss_test=$(curl -s "http://localhost:8000/echo?msg=<script>alert('XSS')</script>")
    if echo "$xss_test" | grep -q "&lt;script&gt;"; then
        echo "✅ XSS FIXED: Script tags are properly escaped"
    else
        echo "❌ XSS VULNERABLE: Script tags are not escaped"
    fi

    echo ""
    echo "4. TESTING NORMAL OPERATION:"
    curl -s "http://localhost:8000/search?q=apple" | \
      python3 -c "import sys, json; data=json.load(sys.stdin); print('Normal search results:', len(data['items']))"
}

wait_for_app
run_tests

echo ""
echo "================================================"
echo "SECURITY TESTS COMPLETED"
echo "================================================"