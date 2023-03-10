# Loopback audio Linux

## Install sink-loopback devices

Add sink device
```shell
pacmd load-module module-null-sink sink_name=VOutput
```

This allows one to route audio from a source directly back to a sink. 
```shell
pacmd load-module module-loopback sink=VOutput
```

Update meta of device
```shell
pacmd update-sink-proplist VOutput device.description=VOutput
pacmd update-sink-proplist VOutput alsa.name=VOutput
```

## Configure pulseaudio

Open pulse audio control

```shell
pavucontrol
```

Configure gqrx audio output to be the new virtual audio output.

Configure default audio input to be the new virtual audio output. 


## Documentation

https://askubuntu.com/questions/257992/how-can-i-use-pulseaudio-virtual-audio-streams-to-play-music-over-skype

https://github.com/toadjaune/pulseaudio-config/blob/master/pulse_setup.sh