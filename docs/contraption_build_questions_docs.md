# Contraption Filament Winder Project - Build Questions & Troubleshooting Documentation

## Bill of Materials and Sourcing

### Community-Maintained BOM
- **Primary Source**: Community-maintained spreadsheet with detailed parts list
- **Rail Options**: 8-foot rails recommended over standard length for improved rigidity
- **Updates**: BOM includes corrections for stepper motor upgrades and component refinements

### 3D Printing Requirements

#### Material Selection
- **Recommended**: Polycarbonate for maximum rigidity
- **Alternative Options**: ABS or PETG acceptable
- **Print Settings**: 
  - Wall count: 1.2-2mm walls (more important than infill)
  - Infill: 15-20% sufficient
  - Focus on wall thickness over infill percentage for structural integrity

#### Printed Components
- **Electrical Box**: CAD files available on Onshape
- **Custom Parts**: Various mounting brackets and fixtures
- **Material Requirements**: ~6kg of preferred stiff filament

### Mounting and Setup
- **Foundation**: Can sit directly on floor with drop cloth - no bolting required
- **Rubber Feet**: Optional addition, doesn't significantly affect performance
- **Workspace**: Adequate floor space for 8-foot rail system

## Electronics and Control System

### Controller Board Issues and Solutions

#### BTT Octopus Board Problems
**Common Issues:**
- Driver failures causing board detection problems
- Status light not blinking when drivers short
- Port detection failures preventing Cyclone connectivity

**Troubleshooting Approach:**
- Test drivers individually before installation
- Replace entire board if multiple driver failures occur
- Maintain spare drivers for quick replacement

#### TMC Driver Selection and Performance

##### TMC2209 Standard Configuration
- **Current Setting**: 1720mA typical
- **Application**: Standard builds with original motors
- **Limitations**: Current limiting affects larger motor performance

##### TMC5160T Upgrade Path
**Performance Gains:**
- Higher current capability than TMC2209
- Improved performance with larger motors
- **Critical Issue**: Octopus board current limiting reduces effectiveness

**TMC5160T Plus V1.0 Solution:**
- Independent power source connection
- Drops directly into standard board
- **Performance Improvement**: 300% speed increase before motor stuttering
- **Recommendation**: Use TMC5160T Plus for high-performance applications

### Stepper Motor Wiring and Troubleshooting

#### Universal Wiring Issues
**Primary Problem**: Inconsistent stepper motor wiring between manufacturers
- Same model motors may have different pinouts
- Amazon stepper cables frequently incorrect or unreliable
- **Critical Safety**: NEVER plug/unplug steppers with board powered

#### Diagnostic Process
1. **Battery Test**: Use AA battery to verify motor phases and locking
2. **Arduino Test**: Low-voltage testing with L289N driver and Arduino Uno
3. **Resistance Check**: Measure coil resistance (~0.3 ohms indicates shorted coil)
4. **Driver Swap**: Test suspected motor with known-good driver

#### Wiring Solutions
**Standard Approach**: A+ A- B+ B-
**Common Fix**: Swap A+ with A- and B+ with B- if motor vibrates instead of rotating
**Verification**: Motor should spin smoothly by hand when disconnected

### Marlin Firmware Configuration

#### Configuration Challenges
- **Complexity**: Limited knowledge base in community for Marlin configuration
- **Build Failures**: Common issue with configuration compilation
- **Version Compatibility**: Both 2.0.x and 2.1.x bug fix versions tested

#### Critical Settings
- **Driver Types**: Must match physical drivers (TMC2209, TMC5160T, etc.)
- **Current Settings**: Typically 1720mA for TMC2209
- **Steps per mm**: Must be calculated for specific stepper/pulley combinations
- **Acceleration/Speed**: Printer defaults too aggressive for filament winder

#### Troubleshooting Firmware Issues
- Use Andrew Reilley's configuration files as baseline
- Test with pre-compiled firmware before attempting custom builds
- Seek 3D printer community assistance for Marlin-specific problems

## Mechanical Assembly and Alignment

### Mandrel System Setup

#### End Cap Attachment (Critical Missing Documentation)
- **Key Component**: 6.35mm flange coupling connectors required
- **Function**: Attach end caps to center rod with proper friction
- **Source**: Amazon part B07RKWYWHG (4-pack)
- **Installation**: Use pipe clamps to secure end caps to mandrel

#### Belt Tensioning and Drive System
- **Mandrel Drive**: 130mm belt standard
- **Adjustment**: Headstock positioning may need modification for proper belt tension
- **Slipping Issues**: Inadequate tensioning causes positioning errors

### 8-Foot Build Modifications

#### Structural Upgrades Required
- **Rail System**: 3" T-slot bars instead of 2" for improved rigidity
- **Connectors**: All mounting brackets require redesign for larger rails
- **Mandrel Caps**: Extended sleeve length needed for adequate friction

#### Belt System Improvements
- **Drive Components**: Belt clamp slots enlarged for durability
- **Motor Gear**: Increased width to provide clearance for lock ring
- **Performance**: Reduces binding and improves smooth operation

### Carriage and Delivery Head Assembly

#### Bearing Integration
- **Carriage Wheels**: Ball bearing addition reduces friction significantly
- **Delivery Head**: Bearing integration improves rotation smoothness
- **Performance Impact**: Major improvement in overall system operation

#### Alignment Procedures
**Delivery Head Height:**
- Axis of rotation must align with mandrel centerline
- Critical for proper fiber placement and wind quality

**Belt Alignment:**
- Timing belt must track properly on pulleys
- Idler bearing positioning prevents belt slippage
- **Documentation Gap**: Visual assembly references needed

## Advanced Applications and Modifications

### Non-Circular Cross Sections

#### Rectangular Tube Manufacturing
**Software Approach:**
- Calculate circumference of rectangle
- Divide by π to determine effective "diameter"
- Input calculated diameter into Cyclone

**Hardware Challenges:**
- **Delivery Head**: Requires specialized roller design with deep channel
- **Fiber Path**: Dramatic angle changes require robust tow guidance
- **Drive System**: Internal rod centering required to prevent noise/vibration

**Applications:**
- Lightweight carbon fiber ladder construction (6-pound, 8-foot target)
- Structural beams with optimized cross-sections
- Alternative to extruded aluminum profiles

### High-Speed Production Modifications

#### Motor and Driver Upgrades
**Current Systems:**
- Standard: TMC2209 with original steppers
- Upgrade: TMC5160T with 3NM motors (limited by board current)
- High-Performance: TMC5160T Plus with independent power supply

**Performance Scaling:**
- Standard system: Basic production speeds
- TMC5160T: ~10% speed improvement (limited by board)
- TMC5160T Plus: ~300% speed improvement

#### Belt System Upgrades
**Problem**: Slipping at higher speeds/loads
**Solution**: Larger drive belts and pulleys
- **Belt**: McMaster 1840K112
- **Pulley**: Modified from McMaster 6495K104 step file
- **Result**: Improved power transmission and reduced slipping

### Delivery Head Optimization

#### Roller vs Fixed Comb Systems
**Roller Challenges:**
- Catches on tow causing motor stalls
- Step skipping under high torque conditions
- Width optimization critical (too narrow causes fraying, too wide allows walking)

**Alternative Approaches:**
- **Long Arc Shape**: Reduces lateral fiber restriction
- **Bearing Integration**: Reduces friction and improves reliability
- **Custom Profiles**: Optimized for specific fiber types and applications

#### Fiber-Specific Considerations
**Carbon Fiber**: Generally well-behaved with proper roller design
**Fiberglass**: More challenging - tends to twist and bunch over distances >6 inches
**Solution Development**: Ongoing community efforts for improved tow flattening techniques

## Quality Control and Process Optimization

### Layer Understanding and Control
**Cyclone Layer Definition:**
- One "layer" = two physical layers of tow
- Hoop wind: covers mandrel twice (forward and return pass)
- Helical wind: same coverage in different pattern
- **Turnaround Regions**: Only areas with single coverage

### Position Accuracy and Drift
**Acceptable Performance:**
- 7+ layer winds over 1+ hour with minimal drift
- Position errors typically within acceptable tolerance
- **Critical Systems**: High-precision applications may require encoders

**Error Sources:**
- Mandrel belt slipping
- Carriage friction variations
- Mandrel circumference measurement errors
- Set screw slippage under load

### Closed-Loop Control Development
**Future Improvements:**
- Encoder feedback for position verification
- Mid-wind homing capability
- Real-time position correction
- Automated tension management

## Safety and Best Practices

### Electrical Safety
- **Power Management**: Never connect/disconnect steppers with power on
- **Driver Protection**: Use genuine drivers to avoid failures
- **Current Settings**: Match driver capabilities to motor requirements

### Mechanical Safety
- **Loose Components**: Secure all set screws and connections
- **High-Speed Operation**: Ensure no loose wires can be caught in movement
- **Proper Tensioning**: Balance between adequate grip and component stress

### Process Safety
- **Resin Handling**: Follow standard composites safety protocols
- **Ventilation**: Adequate airflow for resin systems
- **PPE**: Standard composite manufacturing protection required

---

*This documentation represents the collective troubleshooting knowledge and build experiences from the contraption community, focusing on practical solutions to common assembly and operation challenges.*