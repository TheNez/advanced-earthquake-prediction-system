# Contributing to Advanced Earthquake Prediction System

Thank you for your interest in contributing to this project! We welcome contributions from the geological, data science, and software development communities.

## 🎯 Ways to Contribute

### 🔬 **Scientific Contributions**
- **Geological Data**: Add more volcanoes, fault lines, or tectonic boundaries
- **Model Improvements**: Enhance ML algorithms or feature engineering
- **Validation**: Test predictions against real geological events
- **Research**: Add scientific papers or geological references

### 💻 **Technical Contributions**
- **Code Quality**: Improve performance, readability, or documentation
- **New Features**: Add visualization tools, data sources, or analysis methods
- **Bug Fixes**: Report and fix issues in prediction algorithms
- **Testing**: Add unit tests or integration tests

### 📚 **Documentation & Education**
- **Tutorials**: Create guides for specific use cases
- **Examples**: Add more location-specific analyses
- **Explanations**: Improve scientific explanations for general audiences
- **Translations**: Help make the project accessible to more users

## 🚀 Getting Started

### Development Setup
```bash
# Fork and clone the repository
git clone https://github.com/your-username/earthquake-prediction-system.git
cd earthquake-prediction-system

# Create development environment
python3 -m venv dev_env
source dev_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies (if available)
pip install -r requirements-dev.txt

# Run tests to ensure everything works
python -m pytest tests/ -v
```

### Making Changes
1. **Create a branch** for your feature: `git checkout -b feature/your-feature-name`
2. **Make your changes** following our coding standards
3. **Test thoroughly** to ensure nothing breaks
4. **Document your changes** in code comments and README if needed
5. **Commit with clear messages**: `git commit -m "Add: volcanic risk calculation for XYZ region"`

## 📝 Coding Standards

### Python Code Style
- Follow **PEP 8** Python style guidelines
- Use **meaningful variable names** (e.g., `volcanic_risk_index` not `vri`)
- Add **docstrings** for all functions and classes
- Include **type hints** where appropriate
- Keep functions **focused and small** (< 50 lines when possible)

### Documentation
```python
def calculate_volcanic_influence(self, lat: float, lon: float) -> tuple[float, float, int]:
    """
    Calculate volcanic influence on earthquake risk for a given location.
    
    Args:
        lat (float): Latitude in decimal degrees
        lon (float): Longitude in decimal degrees
        
    Returns:
        tuple: (volcanic_risk_index, nearest_volcano_distance, active_volcanoes_nearby)
        
    Example:
        >>> predictor = AdvancedEarthquakePredictor()
        >>> risk, distance, count = predictor.calculate_volcanic_influence(45.0, -122.0)
        >>> print(f"Risk: {risk:.2f}, Distance: {distance:.1f}km, Count: {count}")
    """
```

## 🔍 Testing Guidelines

### Adding Tests
- **Unit tests** for individual functions
- **Integration tests** for system components
- **Data validation** tests for geological accuracy
- **Performance tests** for large datasets

### Test Structure
```python
import pytest
from advanced_earthquake_predictor import AdvancedEarthquakePredictor

def test_volcanic_influence_calculation():
    """Test volcanic influence calculation for known locations."""
    predictor = AdvancedEarthquakePredictor()
    
    # Test near Mount St. Helens
    risk, distance, count = predictor.calculate_volcanic_influence(46.2, -122.18)
    
    assert risk > 0, "Should have volcanic risk near Mount St. Helens"
    assert distance < 50, "Should be close to Mount St. Helens"
    assert count > 0, "Should detect nearby active volcanoes"
```

## 🌍 Data Contributions

### Adding Volcanic Data
When adding new volcanoes, please include:
- **Accurate coordinates** (decimal degrees)
- **Last eruption date** (year, or negative for BCE)
- **VEI rating** (Volcanic Explosivity Index)
- **Current status** (active/dormant/extinct)
- **Reliable sources** for all data

### Geological Accuracy
- **Verify coordinates** against multiple sources
- **Cross-reference** eruption dates with official records
- **Include source citations** in code comments
- **Test impact** on existing predictions

## 🐛 Reporting Issues

### Bug Reports
Please include:
- **Python version** and operating system
- **Complete error message** and stack trace
- **Steps to reproduce** the issue
- **Expected vs actual behavior**
- **Sample input data** if relevant

### Feature Requests
Please describe:
- **Use case** and motivation
- **Proposed implementation** approach
- **Potential impact** on existing functionality
- **Alternative solutions** considered

## 📋 Pull Request Process

1. **Update documentation** for any new features
2. **Add or update tests** for your changes
3. **Ensure all tests pass** locally
4. **Update CHANGELOG.md** with your changes
5. **Request review** from maintainers

### PR Template
```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Geological Accuracy
- [ ] Data sources verified
- [ ] Cross-referenced with scientific literature
- [ ] Impact on predictions assessed
```

## 🔬 Scientific Standards

### Data Sources
- **Primary sources** preferred (USGS, NOAA, geological surveys)
- **Peer-reviewed publications** for scientific methods
- **Recent data** (within 5 years when possible)
- **Multiple source verification** for critical data

### Model Validation
- **Cross-validation** with independent datasets
- **Comparison** with existing geological models
- **Documentation** of assumptions and limitations
- **Uncertainty quantification** where appropriate

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion
- **Code Review**: Maintainers will provide feedback on PRs
- **Scientific Questions**: Tag issues with `geological-science` label

## 🏆 Recognition

Contributors will be:
- **Listed** in CONTRIBUTORS.md
- **Credited** in release notes
- **Thanked** in documentation updates
- **Invited** to participate in project direction discussions

## 📚 Resources

### Geological References
- [USGS Earthquake Hazards](https://earthquake.usgs.gov/)
- [Global Volcanism Program](https://volcano.si.edu/)
- [International Seismological Centre](http://www.isc.ac.uk/)

### Technical Resources
- [Python Seismology](https://docs.obspy.org/)
- [Scikit-learn Documentation](https://scikit-learn.org/)
- [Geospatial Python](https://geopandas.org/)

Thank you for contributing to advancing earthquake risk assessment tools! 🌍
