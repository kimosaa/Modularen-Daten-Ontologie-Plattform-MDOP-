# Senior Compass App - Product Requirements Document (PRD)

## Overview

The Senior Compass App is designed with accessibility as the core principle, targeting seniors with varying levels of digital literacy, mild arthritis, and cognitive load challenges. This document outlines the key features, user flows, and technical architecture.

---

## 1. 🏡 Home Screen UI Wireframe (Simplified)

The Home Screen adheres to the principles of **Visual Simplicity**, **High Contrast**, and **Large Tappable Areas**. The default color scheme uses high-contrast dark text on a light background.

| Component | Description | Accessibility Notes |
|-----------|-------------|---------------------|
| **Header** | Large, legible time/date. No complex menu bar. | Min 32pt font. |
| **1. Emergency Button** | Large Red Circle at the top right. Label: "HELP - 2 Second Hold". | Always visible. Haptic feedback on tap/hold. |
| **2. One-Touch Call** | Largest Button (Photo & Name). Default pre-set to "David". | Min 180x180 px. Photo-based for recognition. |
| **3. Health Manager** | Large Square Button. Icon: Pill/Clock. Label: "Medicines & Appointments". | Min 24pt font. Color: High-Contrast Green. |
| **4. Utilities** | Large Square Button. Icon: Magnifying Glass. Label: "Magnifier & News". | Min 24pt font. Color: High-Contrast Blue. |
| **5. Photo Stream Preview** | Smallest area, showing the single latest photo. Tapping navigates to the Album. | Simple "New Photo" badge if unviewed. |

### Key Design Principles

- **Minimum Font Size**: 24pt for all labels, 32pt for headers
- **Minimum Touch Target**: 180x180px for primary actions
- **Color Contrast**: WCAG AAA compliant (7:1 contrast ratio)
- **Single-Purpose Screens**: Each screen focuses on one task
- **Audio Feedback**: Confirmatory sounds for all actions
- **Haptic Feedback**: Tactile confirmation for button presses

---

## 2. 💊 User Flow: Adding a Medication

This flow is designed to be **sequential** and utilize **large, single-choice buttons** to accommodate mild arthritis and cognitive load challenges (Evelyn, 78).

| Step | User Action | System Response & UI | Accessibility Notes |
|------|-------------|----------------------|---------------------|
| **1. Initiate** | Taps "Medicines & Appointments" on Home Screen. | Navigates to Health Manager Menu. | Confirmation chime (audio feedback). |
| **2. Select Task** | Taps large button: "Add New Medication". | Navigates to "Medication Name" input screen. | Full-screen, single-purpose view. |
| **3. Name** | Taps large input field and uses the simplified, high-contrast keyboard (or voice input). Enters "Amlodipine". Taps "Next". | Input Confirmation: Audio feedback ("Amlodipine entered"). Saves name. Navigates to dosage. | Clear, simple, sans-serif font (min 24pt). |
| **4. Dosage** | Taps one of the large pre-set buttons: "5mg", "10mg", or taps "Other" for manual input. Selects "5mg". Taps "Next". | Saves dosage. Navigates to schedule. | Large Tappable Buttons to avoid typing errors. |
| **5. Time** | Taps the large clock widget to set the time (e.g., 9:00 AM). Taps "Confirm". | Displays time as large text ("Every Day at 9:00 AM"). | Simplified Time Picker (large, high-contrast numbers). |
| **6. Review & Save** | Review Screen: Displays name, dosage, and time. Taps large button: "Save Reminder". | Confirmation Message: Full-screen pop-up: "Amlodipine Reminder Saved! ✓ Checkmark Icon." Haptic pulse and affirmative sound. | Clear language and explicit success feedback. |

### Flow Characteristics

- **Linear Navigation**: Users cannot skip steps or go back accidentally
- **Persistent Progress**: Each step auto-saves to prevent data loss
- **Voice Input Option**: Available at every text input step
- **Error Prevention**: Pre-set options reduce typing errors
- **Clear Feedback**: Visual, audio, and haptic confirmation at each step

---

## 3. ☁️ Backend and Data Synchronization Architecture

The architecture prioritizes **security**, **data consistency**, and **minimal latency** for critical features (Emergency, Communication, Reminders).

### Core Components

#### 1. Mobile Client (Swift/Kotlin)
- Manages local caching and encryption
- Communicates exclusively with the API Gateway
- Offline-first architecture for critical features
- Local storage for medication reminders

#### 2. API Gateway
- Single entry point for all requests
- Authentication: OAuth 2.0/Token-based
- Rate limiting to prevent abuse
- Request routing to appropriate microservices

#### 3. Microservices Layer

**Communication Service**
- Manages contact lists
- Video call setup (using WebRTC signaling server proxy)
- Family sharing permissions
- Real-time messaging

**Health Service**
- Stores and manages medication schedules
- Appointment data management
- Push notification scheduling
- Integration with health tracking devices

**Location/Safety Service**
- Receives and encrypts GPS pings
- Manages emergency contact list
- Alert protocol and escalation
- Geofencing for safety zones

**Photo/File Service**
- Stores encrypted photos (S3/Blob Storage)
- Metadata management
- Automatic family sharing based on preferences
- Photo compression and optimization

#### 4. Database Layer

**PostgreSQL (Relational)**
- User accounts and authentication
- Metadata storage
- Core configuration (contact settings, roles)
- Transaction data

**DynamoDB/Cassandra (NoSQL)**
- High-volume time-series data
- GPS pings and location history
- Audit logs
- Analytics data

#### 5. Notification Service
- **APNS** (Apple Push Notification Service)
- **FCM** (Firebase Cloud Messaging)
- Reliable, persistent reminders for medications
- Emergency alerts with escalation
- Family notifications for important events

#### 6. Family Web Portal
- Separate web application
- Accesses same API Gateway
- Restricted to viewing opt-in data:
  - Location (if enabled)
  - Photo Stream (if shared)
  - Health Schedule (if shared)
- **Cannot** modify senior's core settings
- Read-only access with audit logging

### Data Synchronization and Encryption

#### Encryption Strategy

**At Rest**
- Database encryption (AES-256)
- File storage encryption (S3 server-side encryption)
- Local device encryption (iOS Keychain, Android Keystore)

**In Transit**
- TLS 1.3 for all communications
- Certificate pinning for mobile clients
- End-to-end encryption for sensitive health data

#### Synchronization Mechanism

**Pull-on-Demand**
- Photo Album syncs on app launch or pull-to-refresh
- Contact list updates on app open
- Settings sync on demand

**Push-on-Change**
- Health Service immediately pushes updates to family portal
- Medication schedule changes sync instantly
- Emergency alerts have highest priority
- Location updates push every 5 minutes (configurable)

**Conflict Resolution**
- Last-write-wins for user preferences
- Server authoritative for health data
- Local-first for emergency features

### Security Measures

1. **Authentication**: Multi-factor authentication optional for family members
2. **Authorization**: Role-based access control (RBAC)
3. **Audit Logging**: All data access logged and monitored
4. **Data Retention**: Configurable retention policies
5. **GDPR Compliance**: Right to deletion and data export
6. **HIPAA Compliance**: Health data encrypted and access-controlled

### Scalability Considerations

- **Horizontal Scaling**: Microservices can scale independently
- **Caching**: Redis for frequently accessed data
- **CDN**: CloudFront for photo delivery
- **Load Balancing**: Auto-scaling based on demand
- **Database Sharding**: User-based sharding for scale

---

## 4. User Personas

### Primary Persona: Evelyn (78)

**Background**
- Retired teacher
- Lives independently
- Basic smartphone experience
- Mild arthritis in hands
- Wears reading glasses

**Needs**
- Large, easy-to-tap buttons
- Clear, simple language
- Audio confirmation
- Medication reminders
- Easy family contact

**Frustrations**
- Small text and buttons
- Complex navigation
- Accidental taps
- Technical jargon
- Multi-step processes

### Secondary Persona: David (52)

**Background**
- Evelyn's son
- Busy professional
- Tech-savvy
- Lives 2 hours away

**Needs**
- Peace of mind about mother's safety
- Medication adherence monitoring
- Easy check-ins
- Emergency alerts
- Photo sharing

**Frustrations**
- Worried about falls
- Can't visit often
- Phone calls interrupted
- Complex elder care apps

---

## 5. Success Metrics

### User Engagement
- Daily active users (DAU)
- Average session duration
- Feature adoption rates
- Medication reminder completion rate

### User Satisfaction
- App Store ratings
- Net Promoter Score (NPS)
- Customer support tickets
- User feedback sentiment

### Technical Performance
- App crash rate < 0.1%
- API response time < 200ms
- Push notification delivery > 99.9%
- App load time < 2 seconds

### Safety & Health
- Emergency response time
- Medication adherence rate
- Family engagement level
- Fall detection accuracy

---

## 6. Future Enhancements

### Phase 2
- Voice-first interface
- Health vitals integration (blood pressure, glucose)
- Advanced fall detection
- AI-powered health insights

### Phase 3
- Integration with smart home devices
- Telemedicine integration
- Social features (senior community)
- Cognitive health games

### Phase 4
- Wearable device integration
- Predictive health alerts
- Care coordination platform
- Insurance integration

---

## 7. Compliance & Privacy

### Regulations
- **HIPAA**: Health data protection
- **GDPR**: European data privacy
- **CCPA**: California privacy rights
- **ADA**: Accessibility standards

### Privacy Features
- Granular permission controls
- Opt-in for all sharing
- Data export capability
- Account deletion
- Transparent data usage

---

## Conclusion

The Senior Compass App is designed to empower seniors to live independently while providing peace of mind to their families. By prioritizing accessibility, simplicity, and security, the app creates a bridge between generations through technology that respects the needs and capabilities of all users.

---

**Document Version**: 1.0
**Last Updated**: 2025-11-10
**Status**: Implementation Ready
