# Contributing to Locust Performance Framework

Thank you for your interest in contributing! This guide will help you get started.

## Code of Conduct

Be respectful, inclusive, and professional. We're building a community of QA engineers.

## How to Contribute

### 🐛 Found a Bug?
1. Check if it's already reported in [Issues](https://github.com/pritamdharme/locust-performance/issues)
2. If not, create a new issue with:
   - Clear title describing the bug
   - Steps to reproduce
   - Expected vs. actual behavior
   - Python version & OS

### ✨ Have an Idea?
1. Open an issue with label `enhancement`
2. Describe the use case and expected behavior
3. Wait for feedback before starting work

### 🔧 Ready to Code?

#### Setup Your Environment
```bash
git clone https://github.com/pritamdharme/locust-performance.git
cd locust-performance
pip install -r requirements.txt
cp .env.example .env
```

#### Branch Naming
```
feature/add-jwt-auth
fix/timeout-handling
docs/update-readme
```

#### Code Style
- Follow **PEP 8** guidelines
- Use clear variable names
- Add docstrings to functions
- Keep functions focused (single responsibility)

#### Example: Adding a New Persona
```python
class GuestCheckoutUser(HttpUser):
    """
    Guest user who checks out without account.
    Simulates 10% of traffic on holiday weekends.
    
    Run with:
      locust -f locustfiles/booking_load.py GuestCheckoutUser --headless -u 50
    """
    
    @task
    def guest_browse_and_checkout(self):
        # Your test code here
        pass
```

#### Testing Your Changes
```bash
# Run a quick smoke test
locust -f locustfiles/booking_load.py --headless -u 10 -r 5 --run-time 1m
```

#### Commit & Push
```bash
git add .
git commit -m "feat: add guest-checkout user persona"
git push origin feature/guest-checkout
```

#### Submit PR
1. Go to the repository and click **Pull Request**
2. Include:
   - What problem does this solve?
   - How did you test it?
   - Any breaking changes?
3. Link any related issues

## PR Requirements

- [ ] Code follows PEP 8 style guidelines
- [ ] Functions have docstrings
- [ ] Changes are tested (provide command used)
- [ ] README updated if behavior changed
- [ ] No hardcoded secrets/credentials

## Questions?

Create a **Discussion** in the repository or reach out:  
📧 pritamdharme@gmail.com

---

**Let's build great performance tests together!** 🚀
