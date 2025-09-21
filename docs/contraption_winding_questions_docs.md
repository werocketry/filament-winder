# Contraption Filament Winder Project - Winding Questions & Process Documentation

## Wind Pattern Analysis and Troubleshooting

### Common Wind Pattern Issues

#### Overlapping Fibers and Gaps
**Symptoms:**
- Biased overlaps in same direction across entire wind
- Bare diamond patterns between fiber paths
- Incomplete coverage despite full layer specification

**Root Cause Analysis:**
1. **Mandrel Slipping**: Primary cause of biased overlaps
2. **Incorrect Steps/mm**: Mandrel not rotating commanded distance
3. **Low Tow Tension**: Causes loose wrapping and uneven placement

**Diagnostic Methods:**
- **Basic Test**: Draw line on mandrel, send `G0 Y360`, verify return to same position
- **Extended Test**: Send `G0 Y3600` (10 rotations) for more accurate measurement
- **Load Test**: Test 100 rotations with tow attached to simulate actual winding resistance

### Mandrel Setup and Calibration

#### Steps Per Millimeter Configuration
**Verification Process:**
- One full rotation should occur with `Y360` command
- Extended testing recommended for cumulative error detection
- Load testing essential to identify slipping under tow tension

#### Pipe Clamp Integration
**Critical Missing Component:**
- Pipe clamps required to secure end caps to mandrel
- Significantly improves grip and prevents slipping
- **Essential Hardware**: Often overlooked in initial builds

#### Flange Coupling System
**Hardware Required:**
- 6.35mm flange coupling connectors (Amazon B07RKWYWHG)
- Attaches end caps to center rod
- **Critical Documentation Gap**: Not included in original CAD files

### Tow Handling and Tension Management

#### Fiber Quality Impact
**Fresh vs Reused Tow:**
- Reused fiber causes bunching and inconsistent width
- Fresh tow essential for quality winds
- Reused fiber acceptable only for dry testing

#### Tension Optimization
**Measurement Methods:**
- Visual assessment of wrap tightness
- Resistance testing during winding
- **Challenge**: No standardized tension measurement protocol in community

**Tension Issues:**
- Low tension: Loose wrapping, uneven coverage
- High tension: Motor stalling, step skipping
- Variable tension: Inconsistent tow width

#### Tow Width Consistency
**Flat Tow vs Twisted Tow:**
- **Flat Tow**: 8mm wide, consistent laydown (18-24k carbon)
- **Twisted/Yarn Tow**: Inconsistent width, difficult to control
- **Performance**: Flat tow provides immediate improvement in wind quality

**Width Specification:**
- Manufacturer specs often inaccurate (6mm tow laying down as 3mm)
- Empirical measurement required for Cyclone parameters
- Width consistency critical for gap-free coverage

### Cyclone Software Configuration and Usage

#### Layer Definition Understanding
**Critical Concept:**
- One Cyclone "layer" = two physical tow layers
- Hoop wind: covers mandrel twice (forward and return)
- Helical wind: same coverage in different pattern
- Turnaround regions: only single coverage

#### Wind File Parameter Optimization
**Example Working Configuration:**
```json
{
    "layers": [{
        "windType": "helical",
        "windAngle": 55,
        "patternNumber": 1,
        "skipIndex": 1,
        "lockDegrees": 360,
        "leadInMM": 15,
        "leadOutDegrees": 90,
        "skipInitialNearLock": true
    }],
    "mandrelParameters": {
        "diameter": 88.90,
        "windLength": 254
    },
    "towParameters": {
        "width": 4.5,
        "thickness": 0.154
    },
    "defaultFeedRate": 2000
}
```

#### Coverage Calculation Methods
**Theoretical Coverage:**
- Width adjusted for wind angle: `width / sin(angle)`
- Number of passes × adjusted width = total coverage
- Must account for mandrel circumference for complete coverage

**Practical Adjustments:**
- Reduce tow width parameter to eliminate gaps
- Account for tow compression and deformation
- Consider lead-in/lead-out effects on coverage

### Advanced Winding Techniques

#### Wind Angle Selection
**Standard Angles:**
- **55°**: Ideal for finite-length pressure vessels (most common)
- **45°**: Alternative for specific applications
- **Lower Angles**: Beneficial for airframe tubes to improve bending resistance

#### Lock Degree Optimization
**Standard Practice:**
- 360° lock degrees most common
- Must be multiple of 360° for proper pattern closure
- Affects turnaround behavior and dogbone formation

#### Dogbone Management
**Characteristics:**
- More dramatic on one end due to algorithm design
- Far end: minimum locking requirement
- Near end: additional material for next start position
- Industry standard: expect to trim ~1 diameter from each end

### Process Timing and Estimation

#### Time Estimation Accuracy
**Expected Performance:**
- Cyclone estimates should be within 5-10% of actual time
- Significant deviations indicate configuration issues
- **Example Issue**: 49-minute estimate completing in 14 minutes suggests steps/mm error

#### Speed Optimization
**Controller Limitations:**
- Arduino boards: insufficient for complex gcode processing
- Small movements processed slowly compared to long moves
- **Solution**: Upgrade to proper printer board (BTT Octopus/SKR)

**Marlin Configuration:**
- Default acceleration settings too conservative
- Z-axis acceleration particularly low (heavy bed assumption)
- Speed limits must match axis capabilities

### Delivery Head Optimization

#### Rotation System Challenges
**Motor Stalling Issues:**
- High current (2A) may still be insufficient for heavy tow rolls
- Friction fit tolerances critical for smooth operation
- Material choice affects consistency (PLA vs PA6-CF)

**Bearing Upgrade Solution:**
- Replace friction fit with bearing system
- 6810-2RS bearings: 50mm ID, 65mm OD, 7mm width
- Eliminates binding through 360° rotation
- Significant improvement in reliability

#### Fiber Path Management
**Pin Design Considerations:**
- Narrow pins: cause fiber catching and fraying
- Wide pins: allow fiber walking and motor stalling
- **Optimal Design**: Long arc shape with minimal lateral restriction
- **Philosophy**: Accurate machine placement preferred over mechanical constraint

### Multiple Mandrel Sizes and Scaling

#### Large Mandrel Considerations (4.5" diameter)
**Speed Requirements:**
- Higher speeds necessary for larger mandrels
- Check max speed configurations for all axes
- Mandrel may run fast while delivery head hits limits

**Tow Behavior Changes:**
- Different tension requirements for larger diameters
- Increased fiber path angles require robust delivery system
- **Performance**: Consistent fiber placement achievable with proper setup

### Quality Control and Validation

#### Visual Inspection Methods
**Pattern Assessment:**
- Fiber alignment consistency
- Gap identification and measurement
- Overlap pattern analysis

**Coverage Verification:**
- Count physical tow paths vs Cyclone predictions
- Compare to plotter output for validation
- Progress bar correlation during winding

#### Plotting and Verification Tools
**Built-in Plotting:**
```bash
npm run cli -- plot -o output.png your_gcode.gcode
```
- Visual representation of planned path
- White space indicates coverage gaps
- Validates Cyclone calculations vs observed results

### Controller and Hardware Considerations

#### Board Upgrade Requirements
**Arduino Limitations:**
- Step processing bottlenecks
- Insufficient for complex motion planning
- **Solution**: BTT Octopus or SKR boards

**Motion Planning:**
- Proper controllers recognize straight-line segments
- Smooth motion despite many small gcode commands
- Pause functionality requires segmented moves

#### Firmware Optimization
**Marlin Configuration Files:**
- Andrew Reilley's configurations available as reference
- Acceleration and speed limits critical for performance
- Steps/mm must match mechanical configuration

### Production Readiness Indicators

#### Successful Wind Characteristics
- Consistent fiber placement and spacing
- Minimal gaps requiring width adjustment only
- Smooth delivery head operation without stalling
- Predictable timing matching Cyclone estimates

#### Pre-Wet Wind Checklist
- Dry wind patterns consistent and gap-free
- All mechanical systems operating smoothly
- Tow tension optimized and stable
- Controller performance validated

---

*This documentation captures the detailed process knowledge and troubleshooting experience from the contraption winding community, focusing on achieving consistent, high-quality wind patterns before proceeding to resin-impregnated production winds.*