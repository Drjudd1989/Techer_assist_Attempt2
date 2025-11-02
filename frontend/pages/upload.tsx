import type { NextPage } from 'next';
import Head from 'next/head';
import styles from '../styles/Home.module.css';
import { useState } from 'react';
import { Geist, Geist_Mono } from "next/font/google";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

const UploadPage: NextPage = () => {
  const [files, setFiles] = useState<FileList | null>(null);
  const [message, setMessage] = useState<string>('');

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFiles(e.target.files);
  };

  const handleUpload = async () => {
    if (!files) {
      setMessage('Please select files to upload.');
      return;
    }

    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
      formData.append('files', files[i]);
    }

    try {
      const response = await fetch('http://localhost:8000/uploadfiles/', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setMessage(data.message);
      } else {
        setMessage('Error uploading files.');
      }
    } catch (error) {
      setMessage('An error occurred while uploading.');
    }
  };

  return (
    <div className={`${styles.page} ${geistSans.variable} ${geistMono.variable}`}>
      <Head>
        <title>Upload Curriculum</title>
        <meta name="description" content="Upload your curriculum files" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>
        <div className={styles.intro}>
          <h1>
            Upload Your Curriculum
          </h1>

          <p>
            Select multiple curriculum files to upload (.pdf, .docx, .txt).
            The AI will use these documents as a knowledge base to generate lesson plans and activities.
          </p>
        </div>

        <div>
          <input type="file" multiple onChange={handleFileChange} />
          <button onClick={handleUpload}>Upload Files</button>
        </div>
        {message && <p>{message}</p>}
      </main>
    </div>
  );
};

export default UploadPage;
