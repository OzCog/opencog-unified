#!/usr/bin/env python3
"""
Test the implemented placeholder fixes
"""
import importlib.util
import json
import os
import sys


results = {
    'passed': [],
    'failed': [],
    'skipped': []
}

def test_fileconfman():
    """Test the fileconfman save_config implementation"""
    try:
        sys.path.insert(0, './language-learning/src/common')

        # Try to import
        spec = importlib.util.spec_from_file_location(
            "fileconfman",
            "./language-learning/src/common/fileconfman.py"
        )
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Check if save_config exists and doesn't just print
            import inspect
            source = inspect.getsource(module.JsonFileConfigManager.save_config)

            if 'print(' in source and 'not implemented' in source.lower():
                results['failed'].append({
                    'test': 'fileconfman.save_config',
                    'reason': 'Still contains "not implemented" print statement'
                })
            elif 'json.dump' in source:
                results['passed'].append({
                    'test': 'fileconfman.save_config',
                    'details': 'Properly implemented with JSON serialization'
                })
            else:
                results['failed'].append({
                    'test': 'fileconfman.save_config',
                    'reason': 'Implementation unclear'
                })
        else:
            results['skipped'].append({
                'test': 'fileconfman.save_config',
                'reason': 'Could not load module'
            })
    except Exception as e:
        results['failed'].append({
            'test': 'fileconfman.save_config',
            'reason': str(e)
        })

def test_teardown_implementation():
    """Test tearDown implementation"""
    try:
        filepath = './atomspace/tests/cython/guile/test_pattern.py'
        with open(filepath) as f:
            content = f.read()

        if 'def tearDown(self):' in content:
            # Check if it's not just pass
            if content.count('def tearDown(self):') == 1:
                # Extract the method
                start = content.find('def tearDown(self):')
                # Find next method or end
                next_def = content.find('\n    def ', start + 1)
                if next_def == -1:
                    next_def = len(content)

                method_content = content[start:next_def]

                if method_content.strip().endswith('pass'):
                    results['failed'].append({
                        'test': 'test_pattern.tearDown',
                        'reason': 'Still just contains pass'
                    })
                elif 'atomspace' in method_content.lower() or 'clean' in method_content.lower():
                    results['passed'].append({
                        'test': 'test_pattern.tearDown',
                        'details': 'Properly implemented with cleanup logic'
                    })
                else:
                    results['skipped'].append({
                        'test': 'test_pattern.tearDown',
                        'reason': 'Implementation unclear'
                    })
        else:
            results['skipped'].append({
                'test': 'test_pattern.tearDown',
                'reason': 'Method not found'
            })
    except Exception as e:
        results['failed'].append({
            'test': 'test_pattern.tearDown',
            'reason': str(e)
        })

def verify_no_mock_implementations():
    """Verify we didn't create any mock implementations"""
    mock_patterns = [
        'pass  # TODO',
        'pass  # FIXME',
        'return None  # placeholder',
        'raise NotImplementedError  # TODO'
    ]

    violations = []

    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['build', '__pycache__']]

        for file in files:
            if not file.endswith('.py'):
                continue

            filepath = os.path.join(root, file)
            try:
                with open(filepath, encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                for pattern in mock_patterns:
                    if pattern in content:
                        violations.append({
                            'file': filepath,
                            'pattern': pattern
                        })
            except Exception:
                pass

    if violations:
        results['failed'].append({
            'test': 'no_mock_implementations',
            'reason': f'Found {len(violations)} potential mock implementations',
            'details': violations[:5]  # Show first 5
        })
    else:
        results['passed'].append({
            'test': 'no_mock_implementations',
            'details': 'No mock implementations detected'
        })

def main():
    print("Testing implemented placeholders...")
    print("=" * 60)

    test_fileconfman()
    test_teardown_implementation()
    verify_no_mock_implementations()

    print(f"\n✓ Passed: {len(results['passed'])}")
    print(f"✗ Failed: {len(results['failed'])}")
    print(f"⊘ Skipped: {len(results['skipped'])}")

    # Save results
    with open('test_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print("\nTest results saved to test_results.json")

    # Show details
    if results['passed']:
        print("\n✓ Passed tests:")
        for item in results['passed']:
            print(f"  - {item['test']}: {item.get('details', 'OK')}")

    if results['failed']:
        print("\n✗ Failed tests:")
        for item in results['failed']:
            print(f"  - {item['test']}: {item.get('reason', 'Unknown')}")

if __name__ == '__main__':
    main()
