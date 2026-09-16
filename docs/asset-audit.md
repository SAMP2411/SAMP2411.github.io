# Visual asset audit

Updated 2026-09-16. Binary files are now available and have been fully decoded locally with Pillow; all SVG files were checked with an XML parser.

## Results

- 69 assets catalogued; 28 assets referenced by current routed pages, project data or the inline homepage scene. All referenced assets pass decoding/XML checks.
- 24 baseline assets retain identical Git blob hashes. No image was recompressed, resampled or otherwise changed by this audit.
- Three original industrial raster assets are corrupt. They remain untouched for preservation, with no current routed-page or project-data references. Existing valid 1600 × 900 WebP alternatives were recovered byte-for-byte from branch `hq-original-project-images`, commit `835584084349e96809a81be2d7ac912b5d997ae3`, and are used under their `-hd-v2.webp` names.
- All nine AI `*-photo-hd.webp` files decode at 1600 × 900. Their retained source WebPs are 360 × 203; the existing EDSR x4 pipeline, crop/resize and sharpening produce enhanced output, not native photographic detail. No additional enhancement was performed.
- `project2.jpg` is actually a valid PNG (887 × 592); file extension and decoded format differ. Existing bytes are preserved.
- `project4.jpg` is stored as 4000 × 3000 JPEG with EXIF orientation. After `ImageOps.exif_transpose`, its displayed dimensions are 3000 × 4000. Use displayed dimensions for HTML aspect ratio.
- `profile.jpg` decodes at 1792 × 2400.
- The new `assets/robotics-scene.svg` is valid XML with a 720 × 600 viewBox, accessible title/description and an explicit conceptual-illustration description.
- Legacy `assets/project/fleet-observability-system.svg` is malformed XML and unused. It remains unmodified; repair it before any future reuse.

## Decode failures retained but unused

| Asset | Failure |
|---|---|
| `assets/project/autonomous-industrial-inspection-hd.webp` | could not create decoder object |
| `assets/project/fleet-observability-system.svg` | not well-formed (invalid token): line 25, column 150 |
| `assets/project/industrial-robot-operations-intelligence-hd.jpg` | cannot identify image file '/workspace/scratch/7c33d256affc/portfolio/assets/project/industrial-robot-operations-intelligence-hd.jpg' |
| `assets/project/robot-fleet-observability-hd.webp` | could not create decoder object |

## Complete inventory

Storage dimensions are decoded raster dimensions; display dimensions account for EXIF rotation. SVG entries show the declared canvas. Baseline references and current references are separately retained in the JSON manifest.

| Asset | Bytes | Storage / canvas | Display | Current refs | Result |
|---|---:|---|---|---:|---|
| `assets/ai/competitive-hd.svg` | 3885 | 0 0 1600 900 | — | 0 | passed |
| `assets/ai/competitive-photo-hd.webp` | 153276 | 1600 × 900 | 1600 × 900 | 4 | passed |
| `assets/ai/competitive.webp` | 5898 | 360 × 203 | 360 × 203 | 0 | passed |
| `assets/ai/dse-hd.svg` | 4804 | 0 0 1600 900 | — | 0 | passed |
| `assets/ai/dse-photo-hd.webp` | 166660 | 1600 × 900 | 1600 × 900 | 13 | passed |
| `assets/ai/dse.webp` | 6106 | 360 × 203 | 360 × 203 | 0 | passed |
| `assets/ai/face-hd.svg` | 3650 | 0 0 1600 900 | — | 0 | passed |
| `assets/ai/face-photo-hd.webp` | 88822 | 1600 × 900 | 1600 × 900 | 3 | passed |
| `assets/ai/face.webp` | 3450 | 360 × 203 | 360 × 203 | 0 | passed |
| `assets/ai/iiot-hd.svg` | 3585 | 0 0 1600 900 | — | 0 | passed |
| `assets/ai/iiot-photo-hd.webp` | 102970 | 1600 × 900 | 1600 × 900 | 3 | passed |
| `assets/ai/iiot.webp` | 3954 | 360 × 203 | 360 × 203 | 0 | passed |
| `assets/ai/jj-hd.svg` | 4152 | 0 0 1600 900 | — | 0 | passed |
| `assets/ai/jj-photo-hd.webp` | 135112 | 1600 × 900 | 1600 × 900 | 0 | passed |
| `assets/ai/jj.webp` | 5138 | 360 × 203 | 360 × 203 | 0 | passed |
| `assets/ai/rst-hd.svg` | 4078 | 0 0 1600 900 | — | 0 | passed |
| `assets/ai/rst-photo-hd.webp` | 106092 | 1600 × 900 | 1600 × 900 | 4 | passed |
| `assets/ai/rst.webp` | 4170 | 360 × 203 | 360 × 203 | 0 | passed |
| `assets/ai/so101-hd.svg` | 4093 | 0 0 1600 900 | — | 0 | passed |
| `assets/ai/so101-photo-hd.webp` | 107700 | 1600 × 900 | 1600 × 900 | 3 | passed |
| `assets/ai/so101.webp` | 4216 | 360 × 203 | 360 × 203 | 0 | passed |
| `assets/ai/turtlebot3-hd.svg` | 3816 | 0 0 1600 900 | — | 0 | passed |
| `assets/ai/turtlebot3-photo-hd.webp` | 82546 | 1600 × 900 | 1600 × 900 | 6 | passed |
| `assets/ai/turtlebot3.webp` | 3084 | 360 × 203 | 360 × 203 | 0 | passed |
| `assets/ai/ur10-hd.svg` | 4008 | 0 0 1600 900 | — | 0 | passed |
| `assets/ai/ur10-photo-hd.webp` | 109020 | 1600 × 900 | 1600 × 900 | 5 | passed |
| `assets/ai/ur10.webp` | 4406 | 360 × 203 | 360 × 203 | 0 | passed |
| `assets/flowcharts/autonomous-industrial-inspection-robot-detailed.svg` | 14480 | 1600 × 900 | — | 2 | passed |
| `assets/flowcharts/autonomous-industrial-inspection-robot.svg` | 6344 | 1600 × 650 | — | 0 | passed |
| `assets/flowcharts/competitive-robotics-detailed.svg` | 11747 | 1600 × 900 | — | 2 | passed |
| `assets/flowcharts/competitive-robotics.svg` | 4934 | 1600 × 650 | — | 0 | passed |
| `assets/flowcharts/distributed-state-estimation-detailed.svg` | 13136 | 1600 × 900 | — | 2 | passed |
| `assets/flowcharts/distributed-state-estimation.svg` | 6013 | 1600 × 650 | — | 0 | passed |
| `assets/flowcharts/iiot-anomaly-detector-detailed.svg` | 11818 | 1600 × 900 | — | 0 | passed |
| `assets/flowcharts/iiot-anomaly-detector-reviewed.svg` | 4285 | 1100 × 940 | — | 2 | passed |
| `assets/flowcharts/iiot-anomaly-detector.svg` | 6172 | 1600 × 650 | — | 0 | passed |
| `assets/flowcharts/industrial-robot-operations-intelligence-detailed.svg` | 15381 | 1600 × 900 | — | 2 | passed |
| `assets/flowcharts/industrial-robot-operations-intelligence.svg` | 8569 | 1600 × 650 | — | 0 | passed |
| `assets/flowcharts/offline-face-recognition-detailed.svg` | 11551 | 1600 × 900 | — | 2 | passed |
| `assets/flowcharts/offline-face-recognition.svg` | 6069 | 1600 × 650 | — | 0 | passed |
| `assets/flowcharts/robot-fleet-observability-platform-detailed.svg` | 13477 | 1600 × 900 | — | 2 | passed |
| `assets/flowcharts/robot-fleet-observability-platform.svg` | 6468 | 1600 × 650 | — | 0 | passed |
| `assets/flowcharts/rst-hackathon-detailed.svg` | 10959 | 1600 × 900 | — | 2 | passed |
| `assets/flowcharts/rst-hackathon.svg` | 5482 | 1600 × 650 | — | 0 | passed |
| `assets/flowcharts/so101-robot-learning-detailed.svg` | 14800 | 1600 × 900 | — | 2 | passed |
| `assets/flowcharts/so101-robot-learning.svg` | 6310 | 1600 × 650 | — | 0 | passed |
| `assets/flowcharts/telepresence-robot-detailed.svg` | 13448 | 1600 × 900 | — | 2 | passed |
| `assets/flowcharts/telepresence-robot.svg` | 6045 | 1600 × 650 | — | 0 | passed |
| `assets/flowcharts/turtlebot3-navigation-detailed.svg` | 12305 | 1600 × 900 | — | 2 | passed |
| `assets/flowcharts/turtlebot3-navigation.svg` | 6171 | 1600 × 650 | — | 0 | passed |
| `assets/flowcharts/unmanned-ground-vehicle-detailed.svg` | 12692 | 1600 × 900 | — | 2 | passed |
| `assets/flowcharts/unmanned-ground-vehicle.svg` | 6025 | 1600 × 650 | — | 0 | passed |
| `assets/flowcharts/ur10-manipulator-detailed.svg` | 13493 | 1600 × 900 | — | 2 | passed |
| `assets/flowcharts/ur10-manipulator.svg` | 6338 | 1600 × 650 | — | 0 | passed |
| `assets/portfolio-ai-sprite.svg` | 10046 | 0 0 800 3150 | — | 0 | passed |
| `assets/project/autonomous-industrial-inspection-hd-v2.webp` | 139960 | 1600 × 900 | 1600 × 900 | 3 | passed |
| `assets/project/autonomous-industrial-inspection-hd.webp` | 15044 | — | — | 0 | failed |
| `assets/project/fleet-observability-system.svg` | 5509 | — | — | 0 | failed |
| `assets/project/industrial-inspection-system.svg` | 4715 | 1600 × 900 | — | 0 | passed |
| `assets/project/industrial-robot-operations-intelligence-hd-v2.webp` | 89078 | 1600 × 900 | 1600 × 900 | 4 | passed |
| `assets/project/industrial-robot-operations-intelligence-hd.jpg` | 15082 | — | — | 0 | failed |
| `assets/project/operations-intelligence-system.svg` | 5408 | 1600 × 900 | — | 0 | passed |
| `assets/project/robot-fleet-observability-hd-v2.webp` | 121170 | 1600 × 900 | 1600 × 900 | 4 | passed |
| `assets/project/robot-fleet-observability-hd.webp` | 15008 | — | — | 0 | failed |
| `assets/robotics-scene.svg` | 7297 | 0 0 720 600 | — | 1 | passed |
| `favicon.svg` | 869 | 0 0 64 64 | — | 16 | passed |
| `profile.jpg` | 2635689 | 1792 × 2400 | 1792 × 2400 | 0 | passed |
| `project2.jpg` | 168713 | 887 × 592 | 887 × 592 | 11 | passed |
| `project4.jpg` | 8473049 | 4000 × 3000 | 3000 × 4000 | 5 | passed |

## Scope of confidence

The decode checks establish valid image data, exact byte hashes and intrinsic dimensions. They do not establish subjective sharpness or factual project evidence. Illustrative AI media must remain labelled. Desktop/mobile crop and appearance checks belong to browser verification. The unused malformed legacy SVG and three corrupt originals are known preserved exceptions, not active rendering dependencies.
