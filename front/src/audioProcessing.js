const bufferToWave = (abuffer, offset, len) => {
    var numOfChan = abuffer.numberOfChannels,
            length = len * numOfChan * 2 + 44,
            buffer = new ArrayBuffer(length),
            view = new DataView(buffer),
            channels = [],
            i,
            sample,
            pos = 0;

    // write WAVE header
    setUint32(0x46464952); // "RIFF"
    setUint32(length - 8); // file length - 8
    setUint32(0x45564157); // "WAVE"

    setUint32(0x20746d66); // "fmt " chunk
    setUint32(16); // length = 16
    setUint16(1); // PCM (uncompressed)
    setUint16(numOfChan);
    setUint32(abuffer.sampleRate);
    setUint32(abuffer.sampleRate * 2 * numOfChan); // avg. bytes/sec
    setUint16(numOfChan * 2); // block-align
    setUint16(16); // 16-bit (hardcoded in this demo)

    setUint32(0x61746164); // "data" - chunk
    setUint32(length - pos - 4); // chunk length

    // write interleaved data
    for (i = 0; i < abuffer.numberOfChannels; i++)
        channels.push(abuffer.getChannelData(i));

    while (pos < length) {
        for (i = 0; i < numOfChan; i++) {
            // interleave channels
            sample = Math.max(-1, Math.min(1, channels[i][offset])); // clamp
            sample = (0.5 + sample < 0 ? sample * 32768 : sample * 32767) | 0; // scale to 16-bit signed int
            view.setInt16(pos, sample, true); // update data chunk
            pos += 2;
        }
        offset++; // next source sample
    }

    // create Blob
    return new Blob([buffer], { type: "audio/wav" });

    function setUint16(data) {
        view.setUint16(pos, data, true);
        pos += 2;
    }

    function setUint32(data) {
        view.setUint32(pos, data, true);
        pos += 4;
    }
  };

const handleCopyRegion = (region, instance) => {
      var segmentDuration = region.end - region.start;

      var originalBuffer = instance.backend.buffer;
      var emptySegment = instance.backend.ac.createBuffer(
          originalBuffer.numberOfChannels,
          Math.ceil(segmentDuration * originalBuffer.sampleRate),
          originalBuffer.sampleRate
      );
      for (var i = 0; i < originalBuffer.numberOfChannels; i++) {
          var chanData = originalBuffer.getChannelData(i);
          var emptySegmentData = emptySegment.getChannelData(i);
          var mid_data = chanData.subarray(
              Math.ceil(region.start * originalBuffer.sampleRate),
              Math.ceil(region.end * originalBuffer.sampleRate)
          );
          emptySegmentData.set(mid_data);
      }

      return emptySegment;
  };

export const regionToBlob = (region, instance) => {
    const cutSelection = handleCopyRegion(region,instance);
    const blob = bufferToWave(cutSelection, 0, cutSelection.length);
    return blob;
}