import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { SafeUrl, DomSanitizer } from '@angular/platform-browser';
import { HttpClient, HttpEventType } from '@angular/common/http';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, CommonModule],
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App {
  protected title = 'ai-coach-app';
  videoUrl: SafeUrl | null = null;
  message: string = '';
  uploadProgress: number = 0;
  isUploading: boolean = false;
  selectedFile: File | null = null;
  apiUrl = 'http://localhost:8000';

  constructor(
    private sanitizer: DomSanitizer,
    private http: HttpClient
  ) {}

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;

    if (input.files && input.files[0]) {
      this.selectedFile = input.files[0];
      const objectUrl = URL.createObjectURL(this.selectedFile);
      this.videoUrl = this.sanitizer.bypassSecurityTrustUrl(objectUrl);
      this.message = '';
      this.uploadProgress = 0;
    }
  }

  onSubmit(): void {
    if (!this.selectedFile) {
      this.message = 'Please select a video file first';
      return;
    }

    this.isUploading = true;
    this.message = 'Uploading video...';
    
    const formData = new FormData();
    formData.append('file', this.selectedFile);

    this.http.post(`${this.apiUrl}/upload-video`, formData, {
      reportProgress: true,
      observe: 'events'
    }).subscribe({
      next: (event) => {
        if (event.type === HttpEventType.UploadProgress && event.total) {
          this.uploadProgress = Math.round(100 * event.loaded / event.total);
        } else if (event.type === HttpEventType.Response) {
          this.message = `Upload successful! Response: ${JSON.stringify(event.body)}`;
          this.isUploading = false;
        }
      },
      error: (error) => {
        console.error('Upload error:', error);
        this.message = `Upload failed: ${error.message || 'Unknown error'}`;
        this.isUploading = false;
      }
    });
  }

  removeVideo(fileInput: HTMLInputElement): void {
    this.videoUrl = null;
    this.message = '';
    if (fileInput) {
      fileInput.value = '';
    }
  }
}
