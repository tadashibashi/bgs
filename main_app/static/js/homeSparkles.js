
window.addEventListener("load", evt => {
    class Sparkle {

        constructor() {
            this.time = 0;
            this.maxTime = .5;
            this.maxSize = 42;
            this.size = 0;
            this.position = {x: 0, y: 0};

            // Refactor into transformable color later
            this.rBegin = 0;
            this.rEnd = 255;
            this.gBegin = 127;
            this.gEnd = 28;
            this.bBegin = 127;
            this.bEnd = 255;
            this.aBegin = 0;
            this.aEnd = 1;
        }

        initRand() {
            this.time = 0;
            this.maxTime = rand(.1, .75);

            this.rBegin = irand(0, 255);
            this.rEnd = irand(0, 255);
            this.gBegin = irand(0, 255);
            this.gEnd = irand(0, 255);
            this.bBegin = irand(0, 255);
            this.bEnd = irand(0, 255);
            this.aBegin = 1;
            this.aEnd = 0;

            this.startSize = 0;
            this.maxSize = irand(10, 40);

            this.position.x = irand(this.maxSize, canvas.width - this.maxSize);
            this.position.y = irand(this.maxSize, canvas.height - this.maxSize);
        }

        initFire() {
            this.time = 0;
            this.maxTime = rand(.1, .5);

            this.rBegin = irand(240, 255)
            this.rEnd = irand(220, 240);
            this.gBegin = 255;
            this.gEnd = 119;
            this.bBegin = 9;
            this.bEnd = 255;
            this.aBegin = 1;
            this.aEnd = 0;

            this.startSize = irand(40, 60)
            this.maxSize = 0;

            this.position.x = irand(10 + canvas.width/2, canvas.width/2 - 25);
            this.position.y = irand(25 + canvas.height/2, canvas.height/2);
        }

        /**
         *
         * @param time {number} in seconds
         */
        update(time) {
            this.time = this.time < this.maxTime ? this.time + time : this.maxTime;
        }

        isExpired() {
            return this.time === this.maxTime;
        }

        render(ctx) {
            if (this.isExpired()) return;
            const percent = Math.min(this.time / this.maxTime, 1);
            const color = "rgba(" + getValue(percent, this.rBegin, this.rEnd) + "," +
                getValue(percent, this.gBegin, this.gEnd) + "," +
                getValue(percent, this.bBegin, this.bEnd) + "," +
                getValue(percent, this.aBegin, this.aEnd) + ")";
            const size = getValue(percent, this.startSize, this.maxSize);
            ctx.beginPath();
            ctx.fillStyle = color;
            ctx.arc(this.position.x, this.position.y, size, 0, 359);
            ctx.closePath();
            ctx.fill();
        }
    }


    const MAX_PARTICLES = 75;

    const canvas = document.querySelector("canvas");
    const ctx = canvas.getContext("2d");
    let active = false;
    let lastTime = 0;
    /**
     *
     * @type {Sparkle[]}
     */
    const sparkles = [];
    const fires = [];
    for (let i = 0; i < MAX_PARTICLES; ++i) {
        sparkles.push(new Sparkle());
        fires.push(new Sparkle());
    }


    function main(time) {
        window.requestAnimationFrame(main);
        const delta = (time - lastTime) * .001;
        lastTime = time;

        if (active) {
            for (let i = 0; i < sparkles.length; ++i) {
                if (sparkles[i].isExpired()) {
                    sparkles[i].initRand();
                    break;
                }
            }

            let count = 10;
            for (let i = 0; i < fires.length; ++i) {
                if (fires[i].isExpired()) {
                    --count;
                    fires[i].initFire();
                    if (count === 0) break;
                }
            }
        }

        // update
        sparkles.forEach(sparkle => {
            sparkle.update(delta);
        });

        fires.forEach(fire => {
            fire.update(delta);
            fire.position.x -= rand(5, 10)*2.15;
            fire.position.y += rand(5, 30);
        });

        // render
        ctx.clearRect(0, 0, canvas.width, canvas.height)
        sparkles.forEach(sparkle => {
            sparkle.render(ctx);
        });

        fires.forEach(fire => fire.render(ctx));

    }

    const rocketImg = document.getElementById("rocket-img");
    rocketImg.addEventListener("mouseenter", evt => {
        active = true;
    });

    rocketImg.addEventListener("mouseleave", evt => {
        active = false;
    })

    main();

    /**
     * @param percent {number}
     * @param min {number}
     * @param max {number}
     * @returns {number}
     */
    function getValue(percent, min, max) {

        return ((max - min) * percent) + min;
    }

    /**
     *
     * @param min {number}
     * @param max {number}
     * @returns {number}
     */
    function rand(min, max) {
        return Math.random() * (max - min) + min;
    }

    /**
     *
     * @param min {number}
     * @param max {number}
     * @returns {number}
     */
    function irand(min, max) {
        return Math.floor(rand(min, max));
    }


});