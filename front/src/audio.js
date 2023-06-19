import React, { useState, useRef, useEffect } from 'react';
import { AudioRecorder } from 'react-audio-voice-recorder';
import WaveSurfer from 'wavesurfer.js';
import RegionsPlugin from 'wavesurfer.js/src/plugin/regions';
import { regionToBlob } from './audioProcessing.js' 

const AudioPlayer = () => {
  const waveformRef = useRef(null);
  const [waveSurfer, setWaveSurfer] = useState(null);
  const [selectedRegion, setSelectedRegion] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [clipsDownloaded, setClipsDownloaded] = useState(0);
  const [fileName, setFileName] = useState('');
  const [nameSubmitted, setNameSubmitted] = useState('');
  const regionLength = 3;
  const regionOptions = {
    start: 0,
    end: regionLength,
    loop: true,
    resize: false,
    color: 'rgba(0,0,0,0.1)',
    minLength: regionLength,
    maxLength: regionLength

  }

  useEffect(() => {
    const waveOptions = {
      container: waveformRef.current,
      waveColor: 'orange',
      progressColor: 'purple',
      height: 200,
      responsive: true,
      normalize: true,
      hideScrollbar: true,
      plugins: [
        RegionsPlugin.create({})
      ]
    };
    const waveSurfer = WaveSurfer.create(waveOptions);
    setWaveSurfer(waveSurfer);

    waveSurfer.on('region-update-end', (region) => {
      setSelectedRegion(region)
    })

    return () => waveSurfer.destroy();
  }, []);
  
  const handlePlayPause = () => {
    if (waveSurfer) {
      if (isPlaying){
        waveSurfer.pause();
      } else {
        waveSurfer.play(selectedRegion.start);
      }
      setIsPlaying(!isPlaying);
    }
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];

    if (waveSurfer && file) {
      addAudioElement(file)
    }
  };

  const addAudioElement = (blob) =>{
    waveSurfer.clearRegions()
    waveSurfer.loadBlob(blob);
    const region = waveSurfer.addRegion(regionOptions);
    setSelectedRegion(region)
  }  
  const handleSetName = (event) => {
    setNameSubmitted(fileName);
    event.preventDefault();
  }
  const handleNameChange = (event) => {
    setFileName(event.target.value)
  }
  
  const handleDownload = () => {
    const blob = regionToBlob(selectedRegion, waveSurfer);
    const wavName = nameSubmitted+"-"+clipsDownloaded+".wav"
    setClipsDownloaded(clipsDownloaded+1);
    var wavURL = window.URL.createObjectURL(blob);
    var tempLink = document.createElement('a');
    tempLink.href = wavURL;
    tempLink.setAttribute('download', wavName);
    tempLink.click();

  }
  
  return (
    <div>
      <AudioRecorder onRecordingComplete={addAudioElement} />
      <form onSubmit={handleSetName}>
        <label>
          Introduce name for the generated clips: 
          <input type="text" value={fileName} onChange={handleNameChange}></input>
        </label>
        <input type="submit" value="submit"></input>
      </form>
      {nameSubmitted && 
        <div> Name set to: {nameSubmitted}</div>
      }
      <input type="file" accept="audio/*" onChange={handleFileChange} />
      <div ref={waveformRef} />
      <button onClick={handlePlayPause}>{isPlaying ? 'Pause' : 'Play'}</button>
      {!isPlaying &&
        <button onClick={handleDownload}>Download</button>
      }
    </div>
  );
};

export default AudioPlayer;