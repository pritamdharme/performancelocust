# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-03-25

### Added
- **4 User Personas**: ReadOnlyUser, BookingUser, AdminUser, AuthStressUser
- **4 Test Scenarios**: Load test, Spike test, Stress test, Soak test
- **Performance Thresholds**: Automated CI gates (P95, P99, failure rate)
- **Authentication Caching**: Token reuse to reduce auth endpoint load
- **GitHub Actions CI/CD Pipeline**: Automated smoke → load → spike progression
- **HTML Reports**: Visual performance metrics exported from each run
- **Interactive UI Mode**: Real-time metrics with web dashboard
- **Headless Mode**: Scripted testing for CI/CD environments
- **Randomised Test Data**: Realistic booking payloads with variance
- **Comprehensive Documentation**: README with setup, scenarios, and best practices
- **Modular Architecture**: Reusable utilities, clean separation of concerns

### Features Included
- ✅ Token-based authentication
- ✅ CRUD operations testing (create, read, update, delete)
- ✅ Admin bulk operations
- ✅ Query parameter filtering
- ✅ Error handling and response validation
- ✅ Weighted task distribution

### Infrastructure
- GitHub Actions CI/CD pipeline
- Environment variable management (.env support)
- Performance thresholds with automatic failures
- Artifact retention for 7-14 days

## [0.1.0] - Initial Concept

### Planned
- Distributed testing across multiple machines
- Custom metrics (business KPIs beyond HTTP)
- Database performance profiling
- Datadog/New Relic integration
- Load test against production (anonymized data)

---

## Roadmap

### Phase 2 (Q2 2025)
- [ ] JWT authentication support
- [ ] GraphQL performance testing
- [ ] Custom metrics framework
- [ ] Real-time Slack notifications

### Phase 3 (Q3 2025)
- [ ] Distributed load generation (multi-region)
- [ ] Database query profiling
- [ ] APM integration (New Relic, Datadog)
- [ ] Cost analysis reporting

---

For information about our versioning policy, see [VERSIONING.md](https://github.com/pritamdharme/locust-performance/wiki/versioning).
