window.onload = () => {
    const video = document.querySelector('#camera');
    const canvas = document.querySelector('#picture');
    const ctx = canvas.getContext('2d');

    function drawLine(ctx, pos, options = { color: "blue", size: 5 }) {
        ctx.strokeStyle = options.color;
        ctx.lineWidth = options.size;

        ctx.beginPath();
        ctx.moveTo(pos.topLeftCorner.x, pos.topLeftCorner.y);
        ctx.lineTo(pos.topRightCorner.x, pos.topRightCorner.y);
        ctx.lineTo(pos.bottomRightCorner.x, pos.bottomRightCorner.y);
        ctx.lineTo(pos.bottomLeftCorner.x, pos.bottomLeftCorner.y);
        ctx.lineTo(pos.topLeftCorner.x, pos.topLeftCorner.y);
        ctx.stroke();
    }

    function checkPicture() {
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const code = jsQR(imageData.data, canvas.width, canvas.height);
        if (code) {
            drawLine(ctx, code.location);
            document.getElementById("shop_id").value = code.data;
            output.style.display = 'block';
            canvas.style.display = 'block';
            video.style.display = 'none';
            video.pause();
        } else {
            setTimeout(checkPicture, 300);
        }
    }

    const constraints = {
        audio: false,
        video: {
            width: canvas.width,
            height: canvas.height,
            facingMode: "environment"
        }
    };

    navigator.mediaDevices.getUserMedia(constraints)
        .then((stream) => {
            video.srcObject = stream;
            video.onloadedmetadata = (e) => {
                video.play();

                checkPicture();
            }
        })
        .catch((err) => {
            console.log(err.name + ": " + err.message);
        });
}