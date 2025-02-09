# TrueSight - Custom Eyewear Measurement System

![TrueSight Demo](demo.gif) <!-- Replace with actual demo GIF/png -->

TrueSight is a web application that uses computer vision and 3D modeling to help users create perfectly fitted eyewear. The system guides users through a face scanning process, provides measurements review, and offers a 3D preview of virtual frames.

## Features

- **Face Scanning**: Real-time webcam face detection with positioning guidance
- **Measurement Calculation**:
  - Eye width measurement
  - Bridge width detection
  - Vertical B-size calculation
- **3D Preview**: Interactive 3D glasses model visualization
- **Measurement Review**: Editable measurement confirmation screen
- **Progress Tracking**: Visual step-by-step progress indicator

## Technologies Used

- **Frontend**:
  - Next.js 14 (App Router)
  - React Three Fiber (3D rendering)
  - Tailwind CSS (Styling)
  - Shadcn UI Components

- **Backend**:
  - Python Flask
  - OpenCV (Face and eye detection)
  - Haar Cascade classifiers

- **3D Modeling**:
  - Onshape CAD integration

## Installation

### Prerequisites
- Node.js v18+
- Python 3.9+
- pip
- Webcam-enabled device

### Frontend Setup
```bash
git clone https://github.com/yourusername/truesight.git
cd truesight/frontend
npm install
```

### Backend Setup
```bash
cd truesight/backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

1. **Start Backend Server**
```bash
cd backend
flask run --port 5000
```

2. **Start Frontend Development Server**
```bash
cd frontend
npm run dev
```

3. Access the application at `http://localhost:3000`

## Application Flow

1. **Home Page** - 3D glasses preview with start button
2. **Face Scan** - Real-time face positioning guidance
3. **Measurements** - Review and edit auto-calculated measurements
4. **Final Review** - 3D model preview with download options

## API Reference

### POST `/api/measure`
**Request:**
```json
{
  "image": "base64-encoded-jpeg-image"
}
```

**Response:**
```json
{
  "eye_width_mm": 62.5,
  "bridge_width_mm": 18.2,
  "b_size_mm": 34.1
}
```

## Measurement Algorithm

The measurement system uses:
1. Haar Cascade classifiers for face/eye detection
2. Hough Circle Transform for iris/pupil detection
3. Pixel-to-millimeter conversion based on:
   - Known average interpupillary distance (63mm)
   - Perspective transformation calculations
   - Facial feature proportional relationships

## Directory Structure

```
truesight/
├── frontend/
│   ├── app/                 # Next.js pages
│   ├── components/          # React components
│   ├── public/              # Static assets
│   └── package.json
├── backend/
│   ├── app.py               # Flask server
│   ├── requirements.txt
│   └── haarcascades/        # OpenCV classifiers
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgements

- OpenCV for computer vision capabilities
- React Three Fiber for 3D visualization
- Onshape for CAD integration
- Haarcascade classifiers contributors
