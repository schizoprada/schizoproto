# Schizoproto -- TODO -- 04/15/2025

## Overall Project Status

### Core Protocol
- [x] Basic URI handling
- [x] Protocol registration templates
- [ ] Full registration implementation
- [ ] Protocol upgrade path (HTTP → WebSocket)
- [ ] Persistence layer

### Render Engine
- [x] Base architecture
- [x] Type system
- [x] Text mutators implementation
- [ ] DOM mutators implementation
- [ ] Target implementations
- [ ] Strategy implementations
- [ ] π-event system completion

### Behavioral Layer
- [ ] User state persistence
- [ ] Interaction tracking
- [ ] Profile building
- [ ] Drift calculation
- [ ] Trigger system

### Distribution
- [ ] Browser extension packaging
- [ ] Standalone application
- [ ] Documentation
- [ ] Examples

## Today's Implementation Goals

### 1. Core Mutators
- [x] Implement Text Mutation System
  - [x] Character corruption (CharacterCorruptor)
  - [x] Word hallucination (WordHallucinator)
  - [x] Sentence manipulation (SentenceShifter)
  - [x] NLP-driven SubstitutionEngine
- [ ] Implement DOMShiftMutator
  - Element reordering
  - Style corruption
  - Attribute manipulation

### 2. Content Targets
- [ ] Implement TextTarget
  - Paragraph selection
  - Sentence parsing
  - Word targeting
- [ ] Implement DOMTarget
  - Element selection
  - Tree traversal
  - Mutation point identification

### 3. Basic Strategy
- [ ] Implement ProgressiveStrategy
  - Combines text and DOM mutations
  - Handles escalation based on interaction count
  - Manages drift application

### 4. Testing
- [ ] Basic unit tests for mutators
- [ ] Integration test for render pipeline
- [ ] Example usage documentation

## Priority for Today:
1. ✓ Complete text mutation system
2. → Proceed with DOM mutators
3. → Implement basic targets
4. → Start on ProgressiveStrategy if time permits
