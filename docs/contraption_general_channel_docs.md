# Contraption Filament Winder Project - General Channel Documentation

## Community Status and Progress Tracking

### Project Website and Resources
- **Primary Documentation**: https://reilley.net/winder/
- **Status**: Pinned resource for comprehensive build information

### Community Build Progress (January 2025 Survey)

#### Active Builders
- **starz**: Multiple tubes wound successfully
- **Bean**: Build complete, calibration and G-code setup in progress
- **LOYDSTER25**: Parts procurement phase, team build planned
- **mrjoso**: Operational winder with completed tubes (36mm and 80mm diameter)
- **AnuvDhariwal**: Hardware mostly complete, electrical integration underway
- **BeepBoopNova**: 3-meter build in progress with curing oven development

#### Build Scale Variations
- **Standard Build**: Original contraption dimensions
- **Extended Build**: 3-meter (3000mm) versions for larger tube production
- **Material Variations**: CNC machined carbon/sandwich composite parts for enhanced rigidity

## Technical Specifications and Limitations

### Diameter Constraints
**Maximum Mandrel Diameter:** ~5 inches (127mm)
**Real Constraint:** Resin pot life vs dispensing rate
- Function of: tow width, machine speed, pot life
- **Design Trade-offs**: Two of three parameters (diameter, length, wall thickness) can be fixed, third is constrained

**Practical Examples:**
- Fixed thickness: 4-foot long 3-inch tube OR 3-foot long 4-inch tube
- Larger diameter/longer tubes require thinner walls

### Resin System Considerations
**Pot Life Solutions:**
- Extended pot life resins: 200-300 minutes available
- Multiple batch strategy for larger builds
- **Critical Issue**: Bottom layers curing before completion

## Build Quality and Performance Issues

### X-Winder Comparison
**Reported Issues:**
- RIT team: ~5 bad tubes per good tube ratio
- Random operation failures
- **Community Goal**: Contraption as reliable alternative

### Electronics Troubleshooting

#### Stepper Motor Issues
**Common Problems:**
- Unidirectional movement with choppy operation
- Delivery head binding issues
- Wiring inconsistencies in Amazon stepper cables

**Diagnostic Process:**
1. Remove gears to isolate motor issues
2. Check mechanical binding in printed parts
3. Verify wiring against motor datasheet
4. **Critical**: Middle two wires frequently incorrect

**Safety Protocols:**
- Limit current to 0.5A during testing
- Avoid hot-plugging steppers
- **Warning**: Enamel smoke from cooked steppers

#### Current Configuration Issues
**Common Error:** Setting current limit to motor rating instead of per-phase rating
- **Example Fix**: 0.8A per motor → 2.8A per phase
- Results in immediate performance improvement

### Wire Management Solutions
**Professional Approach:** Energy chain cable management
**Practical Alternative:** Adequate slack and secure connections
**Field Solution:** Creative stabilization (1-2-3 blocks, temporary weights)

## Material Sourcing and Quality

### Fastener Selection
**Recommended Source:** McMaster-Carr for quality fasteners
**Challenge:** Amazon alternatives typically poor quality
**Investment:** Higher upfront cost for reliable hardware

### Fiber Sources
**Owens Corning Fiberglass:** Available through Amazon
- Tex 1100-158B Type 30 for filament winding applications
- Optimized for epoxy resin systems
- Center-pull spool format unusual but functional

### Shrink Tape Suppliers
**Primary Sources:**
- Soller (shrink tube, not tape)
- Electrowind (variety of shrink percentages)
- Dunstone (temperature-specific options)
**Selection Strategy:** Google search from composites suppliers

## Manufacturing Processes and Techniques

### Demolding Procedures
**Andrew Reilley Method:**
- Phenolic tube mandrels with cleanable mold release
- Hand removal with minimal force required
- Ground surface finish aids release

### Surface Preparation Protocol
**Complete Process:**
1. Cleanable mold release (Stoner E497)
2. Mold release cleaner (Stoner KantStik)
3. Flap wheel sanding (180 grit, 10 seconds)
4. Acetone cleaning
5. IPA final wipe

**Performance Validation:** 3500 psi failure in 3-inch hydrostatic test

### Closure Integration Methods
**Glued Closures:**
- Preferred method over mechanical fasteners
- Requires precise surface preparation
- Higher pressure capability than pinned alternatives

**Mechanical Fasteners:**
- Bolt holes require mandrel modification (pins through drilled holes)
- Challenge: Avoiding case bulging at fastener locations

## Advanced Build Configurations

### CNC Machined Components
**Material:** Carbon fiber/sandwich composites
**Advantages:**
- Greater rigidity than 3D printed parts
- Higher speed operation capability
- 6-point rail mounting eliminates crossbar

### Extended Length Builds
**3-Meter Configurations:**
- Requires heat gun and curing oven integration
- Increased material handling complexity
- Potential for larger production tubes

### Hybrid Material Layups
**Glass/Carbon Combinations:**
- Inner glass layer with outer carbon layer
- **Status**: Experimental concept under consideration

## Future Development: Contraption V2

### Creel System Architecture
**Fundamental Change:** Separate tow spool from carriage motion
**Benefits:**
- Reduced moving mass
- Improved tension control
- Accommodation of large center-pull spools
- Enhanced scalability

### Tension Control System
**Components:**
- Load cell for direct tension measurement
- Controllable brake system (servo-actuated)
- Dancer mechanism for slack management
- **Target Range**: 3N to 15N controllable tension

### Servo-Controlled Brake Design
**Mechanism:** O-ring brake with servo arm tension adjustment
**Testing Results:** 3N to 6N range demonstrated, 15N achievable
**Optimization**: Smaller O-ring for extended range

### Industrial Architecture Adoption
**Reference Design:** Standard industrial filament winder layout
- Stationary creel unit with tension control
- Lightweight carriage with resin bath and delivery head
- **Scalability**: Multiple creel units for increased speed

## Community Problem-Solving Examples

### Cable Management Solutions
**3D Printed Cable Chain:** Effective solution for wire routing
**Source:** Printables.com model 34894 (Drag Cable Chains)
**Performance:** Reliable operation confirmed

### Temporary Stabilization Methods
**Carriage Wobble Solutions:**
- Shimming for alignment correction
- Creative weighting (1-2-3 blocks, toy cars)
- **Focus**: Immediate operational capability over perfect solutions

### Process Interruption Recovery
**Power Loss During Winding:**
- Z-axis motor connection failures
- **Workaround**: Ring winding instead of helical to eliminate third axis
- **Solution**: Improved wire harness design

## Quality Control and Testing

### Hydrostatic Testing Program
**Standard Practice:** Pressure testing of sample sections
**Failure Analysis:** Comparison of glued vs pinned closures
**Performance Benchmarks:** 3500 psi failure pressure achieved

### Mandrel Surface Finish Impact
**Critical Factor:** Mandrel polishing quality
**Issue Example:** Stuck parts due to insufficient surface preparation
**Solution:** Proper mandrel preparation protocols

### Multi-Layer Testing
**Glass/Carbon Experiments:** Under development
**Process Validation:** Progressive complexity increase
**Documentation**: Community sharing of results and methods

---

*This documentation captures the general discussion, community progress, and foundational knowledge shared in the primary contraption channel, serving as the central hub for project status and broad technical discussions.*