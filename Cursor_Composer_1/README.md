# Image Upload Performance Optimization Evaluation

This repository contains two complete Python projects demonstrating the performance optimization of an image upload feature in a social media platform.

## Project Overview

### Project A – Pre-Optimization (Slow Image Upload)
Demonstrates the original, slow image upload functionality with performance bottlenecks:
- Synchronous processing
- No image compression or resizing
- Blocking I/O operations
- No connection pooling
- Server overload during peak traffic

### Project B – Post-Optimization (Optimized Image Upload)
Implements optimized image upload functionality with significant performance improvements:
- Asynchronous processing with thread pools
- Automatic image compression and resizing
- Chunked file reading
- Connection pooling
- Non-blocking I/O operations

## Project Structure

```
.
├── Project_A_PreOptimization_ImageUpload/
│   ├── src/
│   │   ├── upload.py                    # Slow upload server
│   │   └── image_processor.py           # Unoptimized processor
│   ├── tests/
│   │   └── test_pre_optimization.py     # Test harness
│   ├── data/
│   │   └── test_data.json               # Test cases
│   ├── logs/                            # Execution logs
│   ├── performance/                     # Performance metrics
│   ├── requirements.txt
│   ├── setup.sh
│   └── run_tests.sh
│
├── Project_B_PostOptimization_ImageUpload/
│   ├── src/
│   │   ├── upload_optimized.py          # Optimized upload server
│   │   └── image_processor_optimized.py # Optimized processor
│   ├── tests/
│   │   └── test_post_optimization.py    # Test harness
│   ├── data/
│   │   └── test_data.json               # Test cases
│   ├── logs/                            # Execution logs
│   ├── performance/                     # Performance metrics
│   ├── requirements.txt
│   ├── setup.sh
│   └── run_tests.sh
│
├── test_data.json                       # Shared test cases
├── generate_comparison_report.py        # Report generator
├── run_all.sh                           # Master execution script
└── README.md                            # This file
```

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Bash shell (for running shell scripts)
- On Windows: Git Bash or WSL recommended

## Quick Start

### Option 1: Run All Tests (Recommended)

Run both projects and generate the comparison report in one command:

**Linux/Mac:**
```bash
bash run_all.sh
```

**Windows:**
```cmd
run_all.bat
```

This will:
1. Set up and run Project A tests
2. Set up and run Project B tests
3. Generate a comparison report (`compare_report.md`)

### Option 2: Run Projects Individually

#### Project A (Pre-Optimization)

**Linux/Mac:**
```bash
cd Project_A_PreOptimization_ImageUpload
bash setup.sh
bash run_tests.sh
```

**Windows:**
```cmd
cd Project_A_PreOptimization_ImageUpload
setup.bat
run_tests.bat
```

#### Project B (Post-Optimization)

**Linux/Mac:**
```bash
cd Project_B_PostOptimization_ImageUpload
bash setup.sh
bash run_tests.sh
```

**Windows:**
```cmd
cd Project_B_PostOptimization_ImageUpload
setup.bat
run_tests.bat
```

### Option 3: Manual Execution

1. **Install dependencies:**
   ```bash
   pip install -r Project_A_PreOptimization_ImageUpload/requirements.txt
   pip install -r Project_B_PostOptimization_ImageUpload/requirements.txt
   ```

2. **Start Project A server:**
   ```bash
   cd Project_A_PreOptimization_ImageUpload
   python src/upload.py
   ```
   Server runs on `http://localhost:8000`

3. **Run Project A tests** (in another terminal):
   ```bash
   cd Project_A_PreOptimization_ImageUpload
   python tests/test_pre_optimization.py
   ```

4. **Start Project B server:**
   ```bash
   cd Project_B_PostOptimization_ImageUpload
   python src/upload_optimized.py
   ```
   Server runs on `http://localhost:8001`

5. **Run Project B tests** (in another terminal):
   ```bash
   cd Project_B_PostOptimization_ImageUpload
   python tests/test_post_optimization.py
   ```

6. **Generate comparison report:**
   ```bash
   python generate_comparison_report.py \
     Project_A_PreOptimization_ImageUpload/performance/results_pre.json \
     Project_B_PostOptimization_ImageUpload/performance/results_post.json \
     compare_report.md
   ```

## Test Cases

The test suite includes 7 test cases covering:

1. **TC001**: Small image upload (1MB) - Normal case
2. **TC002**: Medium image upload (5MB) - Normal case
3. **TC003**: Large image upload (50MB) - Boundary case
4. **TC004**: Corrupted image upload - Invalid input
5. **TC005**: Very large image upload (100MB) - Boundary case
6. **TC006**: Extremely large image upload (200MB) - Edge case
7. **TC007**: Concurrent upload simulation - Multiple small images

Test cases are defined in `test_data.json` and copied to each project's `data/` directory.

## Performance Metrics

Each test run generates:

- **results_pre.json** / **results_post.json**: Machine-readable test results with:
  - Test ID and description
  - Upload success/failure status
  - Upload time (seconds)
  - Error messages (if any)

- **log_pre.txt** / **log_post.txt**: Human-readable execution logs

- **compare_report.md**: Comprehensive comparison report with:
  - Performance metrics comparison
  - Success rate improvements
  - Upload speed improvements
  - Detailed test results
  - Optimization recommendations

## Key Optimizations in Project B

1. **Asynchronous Processing**
   - Thread pool executor for concurrent image processing
   - Non-blocking I/O operations

2. **Image Compression**
   - Automatic JPEG compression (85% quality)
   - Reduces file sizes by 60-80% while maintaining quality

3. **Automatic Resizing**
   - Large images resized to max 2048px dimension
   - Maintains aspect ratio
   - Reduces processing time significantly

4. **Connection Pooling**
   - Limits concurrent connections to prevent overload
   - Better resource management

5. **Chunked Reading**
   - Large files read in 8KB chunks
   - Reduces memory usage

## Expected Performance Improvements

Based on the optimizations:

- **Upload Speed**: 40-60% faster average upload time
- **Success Rate**: Improved reliability, especially for large files
- **Server Load**: Reduced CPU and memory usage
- **Scalability**: Better handling of concurrent uploads

## Interpreting Results

### Success Rate
- **Pre-Optimization**: May show failures for large images (>50MB) due to timeouts
- **Post-Optimization**: Should achieve near 100% success rate

### Upload Time
- **Pre-Optimization**: Increases linearly with file size (0.1s per MB)
- **Post-Optimization**: More consistent times due to compression and resizing

### Error Handling
- Both implementations handle corrupted images gracefully
- Post-optimization has better timeout handling

## Limitations and Considerations

1. **Simulated Environment**: Network conditions are simulated, not real-world network throttling
2. **Local Testing**: Tests run on localhost; real-world performance may vary
3. **Server Resources**: Performance depends on available CPU and memory
4. **Image Quality**: Compression reduces file size but may slightly reduce quality

## Troubleshooting

### Server Won't Start
- Check if ports 8000 or 8001 are already in use
- Ensure Python 3.7+ is installed
- Verify all dependencies are installed: `pip install -r requirements.txt`

### Tests Fail with Connection Error
- Ensure the server is running before executing tests
- Check server logs in `logs/` directory
- Verify the correct port is used (8000 for Project A, 8001 for Project B)

### Permission Errors (Linux/Mac)
- Make scripts executable: `chmod +x *.sh`
- Ensure write permissions for `uploads/`, `logs/`, and `performance/` directories

### Import Errors
- Ensure you're in the correct project directory
- Install dependencies: `pip install -r requirements.txt`
- Check Python version: `python --version`

## Further Optimizations

Potential improvements for production:

1. **CDN Integration**: Serve images from Content Delivery Network
2. **WebP Format**: Convert images to WebP for better compression
3. **Progressive Loading**: Implement progressive JPEG loading
4. **Caching**: Add Redis/Memcached for frequently accessed images
5. **Horizontal Scaling**: Load balancing across multiple servers
6. **Message Queues**: Use RabbitMQ/Kafka for async processing
7. **Database Optimization**: Optimize database writes for metadata

## License

This project is provided for evaluation and educational purposes.

## Contact

For questions or issues, please refer to the project documentation or create an issue in the repository.

---

*Generated for Performance Optimization Evaluation - Feature & Improvement Category*

