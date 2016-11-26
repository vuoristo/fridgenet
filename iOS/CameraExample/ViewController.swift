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
    var addButton: UIButton?
    var removeButton: UIButton?
    
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
    
    func addButtons() {
        addButton?.frame = CGRect(x: 100, y: 100, width: 100, height: 50)
        addButton?.backgroundColor = UIColor.green
        addButton?.setTitle("Remove", for: UIControlState.normal)
        addButton?.addTarget(self, action: #selector(self.addToInventory), for: UIControlEvents.touchUpInside)
        self.view.addSubview(addButton!)
        
        removeButton?.frame = CGRect(x: 200, y: 100, width: 100, height: 50)
        removeButton?.backgroundColor = UIColor.green
        removeButton?.setTitle("Add", for: UIControlState.normal)
        removeButton?.addTarget(self, action: #selector(self.removeFromInventory), for: UIControlEvents.touchUpInside)
        self.view.addSubview(removeButton!)
    }
    
    func addToInventory(label: String) {
        let parameters: Parameters = [
            "label":label
        ]
        Alamofire.request(ROOT_URL + "/inventory", method: .post, parameters: parameters, encoding: JSONEncoding.default).responseJSON { (response) in
                      switch response.result {
            case .success:
                print("Successfully added!")
            case .failure(let error):
                print(error)
            }
        }
    }
    
    func removeFromInventory(label: String) {
        let parameters: Parameters = [
            "label":label
        ]
        Alamofire.request(ROOT_URL + "/inventory", method: .delete, parameters: parameters, encoding: JSONEncoding.default).responseJSON { (response) in
            switch response.result {
            case .success:
                print("Successfully Removed!")
            case .failure(let error):
                print(error)
            }
        }
    }
    
    func itemFound(label: String) {
        let alert = UIAlertController(title: "Would you like to add or remove the " + label + "?", message: label, preferredStyle: UIAlertControllerStyle.alert)
        alert.addAction(UIAlertAction(title: "Add", style: UIAlertActionStyle.default, handler: {(action: UIAlertAction!) in self.addToInventory(label: label)}))
        alert.addAction(UIAlertAction(title: "Remove", style: UIAlertActionStyle.destructive, handler: {(action: UIAlertAction!) in self.removeFromInventory(label: label)}))
    }
    
    
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
        addButton?.bringSubview(toFront: self.view)
        frameCounter += 1
        if frameCounter % 3 == 0 {
            print("Collected \n")
            let image = imageFromSampleBuffer(sampleBuffer: sampleBuffer)
            guard let imageData = UIImageJPEGRepresentation(image, 0.1) else {
                print("Could not get JPEG representation of UIImage")
                return
            }
            let URL = try! URLRequest(url: ROOT_URL + "/detect", method: .post)
            Alamofire.upload(multipartFormData: { (multipartFormData) in
                multipartFormData.append(imageData, withName: "file", fileName: "uploaded_file", mimeType: "image/jpeg")
            }, with: URL, encodingCompletion: { (result) in
                switch result {
                case .success(let upload, _, _):
                    
                    upload.responseJSON { response in
                        if let httpResponse = response.response {
                            if httpResponse.statusCode == 200 {
                                print("KAKSSATAA")
                                print(response.response)
                                print(response.result)
                                self.itemFound(label: response.result.value as! String)
                            }
                            else if httpResponse.statusCode == 204 {
                              print("Nothing found")
                            }
                        }
                        print(response.request ?? "qweqwe")  // original URL request
                        print(response.response ?? "qweqwe") // URL response
                        print(response.data ?? "qweqwe")     // server data
                        print(response.result)   // result of response serialization
                        //                        self.showSuccesAlert()
                        if let JSON = response.result.value {
                            print("JSON: \(JSON)")
                        }
                    }
                    
                case .failure(let encodingError):
                    print(encodingError)
                }            })
            
            
        }
		// Here you collect each frame and process it
	}

	func captureOutput(_ captureOutput: AVCaptureOutput!, didDrop sampleBuffer: CMSampleBuffer!, from connection: AVCaptureConnection!) {
        frameCounter += 1
		print("Dropped \n")
	}
	
}

// Networking calls
