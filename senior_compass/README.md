# Senior Compass App

An accessible, senior-friendly application designed to help elderly users live independently while providing peace of mind to their families.

## Project Overview

The Senior Compass App is built with accessibility as the core principle, targeting seniors with varying levels of digital literacy, mild arthritis, and cognitive load challenges. The app features large, tappable buttons, high-contrast UI, audio feedback, and simplified workflows.

## Project Structure

```
senior_compass/
├── app/                    # Mobile app implementation (future)
├── backend/                # Backend services and API (future)
├── card_game/              # Card game module (Python implementation)
│   ├── __init__.py
│   ├── card.py            # Card class
│   ├── deck.py            # Deck class with shuffle/deal
│   ├── player.py          # Player class with hand management
│   ├── game.py            # Base game class
│   ├── demo.py            # Demonstration script
│   └── README.md          # Card game documentation
├── docs/                   # Documentation
│   └── SENIOR_COMPASS_PRD.md  # Product Requirements Document
└── tests/                  # Test suite
    └── test_card_game.py  # Card game unit tests
```

## Features Implemented

### ✅ Card Game Module (Python)

A complete implementation of a card game module featuring:
- **Card**: Single playing card with suit and rank
- **Deck**: Standard 52-card deck with shuffle and deal functionality
- **Player**: Player with hand management
- **Game**: Base game class for solitaire-style games

**Key Features:**
- Clean, modular design
- Full test coverage (21 unit tests)
- Accessibility-focused output
- No external dependencies

**Quick Start:**
```bash
# Run the demo
cd senior_compass/card_game
python demo.py

# Run tests
cd senior_compass/tests
python test_card_game.py
```

### 📋 Product Requirements Document

Comprehensive PRD located at `docs/SENIOR_COMPASS_PRD.md` including:
- **Home Screen UI Wireframe**: Large buttons, high contrast, simple navigation
- **User Flows**: Adding medication with step-by-step walkthrough
- **Backend Architecture**: Microservices, data sync, security
- **User Personas**: Evelyn (78) and David (52)
- **Success Metrics**: Engagement, satisfaction, performance, safety
- **Future Enhancements**: Voice interface, health vitals, telemedicine

## Core Principles

1. **Visual Simplicity**: Clean, uncluttered interface
2. **High Contrast**: WCAG AAA compliant (7:1 contrast ratio)
3. **Large Tappable Areas**: Minimum 180x180px for primary actions
4. **Audio Feedback**: Confirmatory sounds for all actions
5. **Haptic Feedback**: Tactile confirmation for button presses
6. **Single-Purpose Screens**: One task per screen
7. **Error Prevention**: Clear choices, avoid typing where possible

## Key Features (Planned)

### 🏡 Home Screen
- Large time/date display (32pt font minimum)
- Emergency button (2-second hold with haptic feedback)
- One-touch call with photo recognition
- Health manager for medications and appointments
- Utilities (magnifier, news)
- Photo stream preview

### 💊 Health Manager
- Medication reminders with audio alerts
- Appointment scheduling
- Large, sequential input forms
- Voice input support
- Review & confirmation screens

### 🔒 Safety Features
- Emergency contact system
- GPS location sharing (opt-in)
- Fall detection (future)
- Family web portal for monitoring

### 📸 Photo Sharing
- Automatic family photo sync
- Simple album view
- "New photo" notifications

## Technology Stack (Planned)

### Mobile App
- **iOS**: Swift, SwiftUI
- **Android**: Kotlin, Jetpack Compose
- **Offline-first**: Local caching for critical features

### Backend
- **API Gateway**: OAuth 2.0, rate limiting
- **Microservices**: Communication, Health, Location, Photos
- **Databases**: PostgreSQL (relational), DynamoDB (time-series)
- **Storage**: S3/Blob Storage with encryption
- **Notifications**: APNS, FCM

### Security
- TLS 1.3 for all communications
- AES-256 encryption at rest
- End-to-end encryption for health data
- HIPAA and GDPR compliant

## Getting Started

### Prerequisites
- Python 3.8+ (for card game module)
- No external dependencies required

### Running the Card Game Demo

```bash
cd senior_compass/card_game
python demo.py
```

### Running Tests

```bash
cd senior_compass/tests
python test_card_game.py
```

All 21 tests should pass with OK status.

## Documentation

- **[Product Requirements Document](docs/SENIOR_COMPASS_PRD.md)**: Complete app specification
- **[Card Game README](card_game/README.md)**: Card game module documentation

## User Personas

### Primary: Evelyn (78)
- Retired teacher
- Lives independently
- Basic smartphone experience
- Mild arthritis in hands
- Needs large buttons and simple navigation

### Secondary: David (52)
- Evelyn's son, busy professional
- Lives 2 hours away
- Wants peace of mind about mother's safety
- Needs medication monitoring and emergency alerts

## Success Metrics

- **User Engagement**: Daily active users, session duration
- **User Satisfaction**: App Store ratings, NPS
- **Technical Performance**: <0.1% crash rate, <200ms API response
- **Safety & Health**: Medication adherence, emergency response time

## Future Enhancements

### Phase 2
- Voice-first interface
- Health vitals integration
- Advanced fall detection
- AI-powered health insights

### Phase 3
- Smart home integration
- Telemedicine
- Social features (senior community)
- Cognitive health games

### Phase 4
- Wearable device integration
- Predictive health alerts
- Care coordination platform
- Insurance integration

## Compliance

- **HIPAA**: Health data protection
- **GDPR**: European data privacy
- **CCPA**: California privacy rights
- **ADA**: Accessibility standards

## License

[License information to be added]

## Contributing

[Contribution guidelines to be added]

## Contact

[Contact information to be added]

---

**Version**: 1.0.0
**Last Updated**: 2025-11-10
**Status**: Card Game Module - Implementation Complete
**Status**: Mobile App & Backend - Design Phase
