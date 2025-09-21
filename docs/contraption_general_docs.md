# Contraption Filament Winder Project - General Channel Documentation

## Project Overview
The Contraption is an open-source filament winder project created by Andrew Reilley. This Discord server serves as a community hub for people building and discussing contraption-inspired filament winders, primarily used for composite rocket motor cases and other aerospace applications.

## Community Setup and Resources

### Initial Setup (December 2024)
- Discord server created by Andrew Reilley on December 17, 2024
- Originally planned to be linked on r/rocketry and Andrew's website
- Community requested a #resources channel for links to contraption documentation and useful materials

## Technical Discussions and Knowledge Base

### Surface Preparation and Bonding Process

#### Mold Release and Surface Prep (April 2025)
**Andrew Reilley's Recommended Process:**
1. **Mold Release Selection**: Use cleanable mold release during tube manufacturing
   - Recommended: Stoner E497 (produces "bondable"/"paintable" parts)
   - Avoid releases that permeate into surface and cannot be removed
   - Check datasheet for "cleanable" or "bondable" specifications

2. **Bond Preparation Process**:
   - Clean tube interior with Stoner KantStick 1.0 (mold release dissolver)
   - Sand using internal sanding flap wheel (~200 grit) until surface is less shiny
   - Clean dust with acetone + IPA mixture
   - Surface is then ready for bonding

#### Motor Closure Design
- **Sealing Strategy**: O-rings used on both closures (nozzle and forward)
- **Pressure Management**: No intentional gas leakage from liner in this design
- **Tapered Bond Lines**: Testing showed tapered moats for epoxy don't provide significantly different performance vs typical bondlines

### Liner Technology and Integration

#### Liner as Pressure Vessel
- **Design Philosophy**: Liner acts as the primary pressure vessel
- **Manufacturing**: Case is made using liner as mandrel for perfect fit
- **Performance**: 10+ hydrostatic tests and 5 firings completed without liner cracking
- **Tolerance Control**: Perfect case-to-liner fit eliminates need for intentionally leaky liners

#### Spin Cast Liner Considerations
**Challenges Identified:**
- Potentially too soft for O-ring sealing (unconfirmed)
- Tolerancing issues with spin casting process
- Density characterization difficulties with traditional methods

**Solutions and Workarounds:**
- Allow pressure equalization in casing near closures
- Seal closure-to-casing with O-rings instead of liner sealing
- Develop custom density characterization methods using known volumes and measured thicknesses

### Filament Winding Techniques

#### Lock Angle Optimization
- **Standard Practice**: 720° lock degrees commonly used
- **Optimization Opportunity**: Reducing to 360° could save tow material and reduce mass
- **Status**: Experimental concept, no results reported yet

#### Industrial Techniques Observed
- **CTI Filament Winder**: Uses Uline tape gun for applying heat shrink tape
- **Process Observation**: Heat shrink tape application appears to be standard industrial practice

### Advanced Winder Design Concepts

#### Contraption v2 Development Plans
- **Spool Management**: Moving spool off gantry/bogey for improved design
- **Industry Standard**: Majority of serious winders use off-gantry spool systems
- **Requirements**: Slack/tension management system needed for off-gantry design

#### Tension Control Systems
- **Stall Guard Method**: Experimental approach using motor current spikes to detect tension
- **Limitations**: May limit to single tension value rather than variable control
- **Alternative**: Dedicated tension management systems (industry standard)

### Performance Achievements

#### Speed Optimization
- **Current Achievement**: 1km/hr tow speed achieved (September 2025)
- **Bottleneck Identified**: Turnaround optimization needed for further speed improvements
- **Safety Considerations**: Loose wire management critical at high speeds to prevent integration into composite layup

### Real-World Applications

#### UC Davis Engineering Expo (June 2025)
- **Project**: Carbon over-wrapped bamboo for solar panel support
- **Validation**: Demonstrates contraption's versatility beyond rocket motor applications
- **Community Response**: Positive reception of alternative applications

## Project Development Status

### Hardware Testing
- Multiple hydrostatic tests completed successfully
- Live fire testing program ongoing (5 firings documented)
- Various epoxy systems tested (DP420, Proline, E120HP)

### Design Evolution
- Rectangular cross-section tubes achieved
- Speed optimization ongoing
- Community contributions to design improvements

### Safety and Best Practices
- Proper surface preparation protocols established
- Pressure vessel design validated through testing
- Material compatibility verified across multiple systems

## Community Contributions and Collaboration

### Senior Design Projects
- University students incorporating contraption concepts
- Filament winder development as senior capstone projects
- Academic validation of open-source approach

### Knowledge Sharing
- Active technical discussions on manufacturing processes
- Material testing results shared openly
- Troubleshooting support provided by community members

### Future Development
- Documentation formalization in progress
- Transition from Discord to more formal project management
- Open-source development model continuing

---

*This documentation captures the collective knowledge from the general Discord channel as of September 2025. The community continues to evolve and contribute to the contraption filament winder project.*