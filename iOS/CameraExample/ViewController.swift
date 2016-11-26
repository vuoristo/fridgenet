//
//  ViewController.swift
//  CameraExample
//
//  Created by Geppy Parziale on 2/15/16.
//  Copyright © 2016 iNVASIVECODE, Inc. All rights reserved.
//

import UIKit
import AVFoundation
import Alamofire

let ROOT_URL = "https://fridgenet.herokuapp.com"

class ViewController: UIViewController, AVCaptureVideoDataOutputSampleBufferDelegate {
    
    var frameCounter: Int = 0

	override func viewDidLoad() {
		super.viewDidLoad()
		setupCameraSession()
	}

	override func viewDidAppear(_ animated: Bool) {
		super.viewDidAppear(animated)

		view.layer.addSublayer(previewLayer)

		cameraSession.startRunning()
	}

	lazy var cameraSession: AVCaptureSession = {
		let s = AVCaptureSession()
		s.sessionPreset = AVCaptureSessionPreset640x480
		return s
	}()

	lazy var previewLayer: AVCaptureVideoPreviewLayer = {
		let preview =  AVCaptureVideoPreviewLayer(session: self.cameraSession)
		preview?.bounds = CGRect(x: 0, y: 0, width: self.view.bounds.width, height: self.view.bounds.height)
		preview?.position = CGPoint(x: self.view.bounds.midX, y: self.view.bounds.midY)
		preview?.videoGravity = AVLayerVideoGravityResize
		return preview!
	}()

    func setupCameraSession() {
        let captureDevice = AVCaptureDevice.defaultDevice(withMediaType: AVMediaTypeVideo) as AVCaptureDevice


		do {
            let deviceInput = try AVCaptureDeviceInput(device: captureDevice)
            print(captureDevice.activeFormat.videoSupportedFrameRateRanges)
            
            if (cameraSession.canAddInput(deviceInput) == true) {
                cameraSession.addInput(deviceInput)
            }
            
            try captureDevice.lockForConfiguration()
            captureDevice.activeVideoMaxFrameDuration = CMTimeMake(1, 3)
            captureDevice.activeVideoMinFrameDuration = CMTimeMake(1, 3)
            captureDevice.unlockForConfiguration()
			
			cameraSession.beginConfiguration()


			let dataOutput = AVCaptureVideoDataOutput()
			dataOutput.videoSettings = [(kCVPixelBufferPixelFormatTypeKey as NSString) : NSNumber(value: UInt(kCVPixelFormatType_32BGRA))]
			dataOutput.alwaysDiscardsLateVideoFrames = true

			if (cameraSession.canAddOutput(dataOutput) == true) {
				cameraSession.addOutput(dataOutput)
			}

			cameraSession.commitConfiguration()

			let queue = DispatchQueue(label: "com.invasivecode.videoQueue")
			dataOutput.setSampleBufferDelegate(self, queue: queue)

		}
		catch let error as NSError {
			NSLog("\(error), \(error.localizedDescription)")
		}
	}
    
    func imageFromSampleBuffer(sampleBuffer: CMSampleBuffer) -> UIImage {
        // Get a CMSampleBuffer's Core Video image buffer for the media data
        let imageBuffer = CMSampleBufferGetImageBuffer(sampleBuffer)
        // Lock the base address of the pixel buffer
        CVPixelBufferLockBaseAddress(imageBuffer!, CVPixelBufferLockFlags(rawValue: 0))
        
        // Get the number of bytes per row for the pixel buffer
        let baseAddress = CVPixelBufferGetBaseAddress(imageBuffer!)
        
        // Get the number of bytes per row for the pixel buffer
        let bytesPerRow = CVPixelBufferGetBytesPerRow(imageBuffer!)
        // Get the pixel buffer width and height
        let width = CVPixelBufferGetWidth(imageBuffer!)
        let height = CVPixelBufferGetHeight(imageBuffer!)
        
        // Create a device-dependent RGB color space
        let colorSpace = CGColorSpaceCreateDeviceRGB()
        
        // Create a bitmap graphics context with the sample buffer data
        let bitmapInfo = CGBitmapInfo(rawValue: CGImageAlphaInfo.noneSkipFirst.rawValue | CGBitmapInfo.byteOrder32Little.rawValue)
        let context = CGContext(data: baseAddress, width: width, height: height, bitsPerComponent: 8, bytesPerRow: bytesPerRow, space: colorSpace, bitmapInfo: bitmapInfo.rawValue)
        // Create a Quartz image from the pixel data in the bitmap graphics context
        let quartzImage = context!.makeImage();
        // Unlock the pixel buffer
        CVPixelBufferUnlockBaseAddress(imageBuffer!,CVPixelBufferLockFlags(rawValue: 0));
        
        // Create an image object from the Quartz image
        let image = UIImage(cgImage: quartzImage!)
        
        return image
    }
    
    func dataToJSON(data: Data) -> Any? {
        do {
            return try JSONSerialization.jsonObject(with: data as Data, options: .mutableContainers)
        } catch let myJSONError {
            print(myJSONError)
        }
        return nil
    }

	func captureOutput(_ captureOutput: AVCaptureOutput!, didOutputSampleBuffer sampleBuffer: CMSampleBuffer!, from connection: AVCaptureConnection!) {
        frameCounter += 1
        if frameCounter % 3 == 0 {
            print("Collected \n")
            let image = imageFromSampleBuffer(sampleBuffer: sampleBuffer)
            guard let imageData = UIImageJPEGRepresentation(image, 0.1) else {
                print("Could not get JPEG representation of UIImage")
                return
            }
            Alamofire.upload(imageData, to: ROOT_URL + "/detect").responseJSON { response in
                debugPrint(response)
            }
            
        }
		// Here you collect each frame and process it
	}

	func captureOutput(_ captureOutput: AVCaptureOutput!, didDrop sampleBuffer: CMSampleBuffer!, from connection: AVCaptureConnection!) {
        frameCounter += 1
		print("Dropped \n")
	}
	
}

// Networking calls
