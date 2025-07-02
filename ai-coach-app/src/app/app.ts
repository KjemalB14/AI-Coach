import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { SafeUrl, DomSanitizer } from '@angular/platform-browser';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App {
  protected title = 'ai-coach-app';
  videoUrl: SafeUrl | null = null;
  message: string = '';

  constructor(private sanitizer: DomSanitizer) {}

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;

    if (input.files && input.files[0]) {
      const file = input.files[0];
      const objectUrl = URL.createObjectURL(file);
      this.videoUrl = this.sanitizer.bypassSecurityTrustUrl(objectUrl);
      this.message = '';
    }
  }

  onSubmit(): void {
    this.message = 'Video submitted';
  }

  removeVideo(fileInput: HTMLInputElement): void {
    this.videoUrl = null;
    this.message = '';
    if (fileInput) {
      fileInput.value = '';
    }
  }
}
