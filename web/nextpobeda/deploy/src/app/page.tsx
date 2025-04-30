'use client';

import { useEffect, useState } from 'react';
import styles from './page.module.css';

export default function Home() {
  const [time, setTime] = useState(0);
  const [rotation, setRotation] = useState(0);
  const [hue, setHue] = useState(0);
  const [showSecret, setShowSecret] = useState(false);

  useEffect(() => {
    const timerInterval = setInterval(() => {
      setTime(prevTime => prevTime + 1);
    }, 100);

    const rotationInterval = setInterval(() => {
      setRotation(prevRotation => (prevRotation + 5) % 360);
    }, 50);

    const hueInterval = setInterval(() => {
      setHue(prevHue => (prevHue + 3) % 360);
    }, 100);

    const secretInterval = setInterval(() => {
      setShowSecret(Math.random() > 0.9);
    }, 10);

    return () => {
      clearInterval(timerInterval);
      clearInterval(rotationInterval);
      clearInterval(hueInterval);
      clearInterval(secretInterval);
    };
  }, []);

  return (
    <main
      className={styles.main}
      style={{ filter: `hue-rotate(${hue}deg)` }}
    >
      <div className={styles.noiseOverlay}></div>

      <div className={styles.container} style={{ transform: `rotate(${Math.sin(time * 0.01) * 3}deg)` }}>
        <h1 className={styles.title}>
          <span className={styles.blink}>СЛЕДУЮЩИЙ</span>
          <span className={styles.shake}>J</span>
          <span className={styles.rotate}>S</span>
        </h1>

        <div className={styles.timer}>
          {time.toString().padStart(5, '0')}
        </div>

        <div className={styles.content}>
          <p className={styles.text} style={{ transform: `skew(${Math.sin(time * 0.05) * 15}deg)` }}>
            РАСТПОБЕДА НЕВОЗМОЖНА НА 1905%
          </p>
          <p className={styles.text}>ЗАГРУЗКА МОЗГА НА 146%</p>
          <p className={styles.text} style={{ fontSize: `${Math.abs(Math.sin(time * 0.03) * 3) + 1.5}rem` }}>
            СЛЕДУЮЩИЙ РУЛИТ МИР
          </p>
          <p className={styles.text}>ВСЕ БУДЕТ <span className={styles.glitch}>ДЖАВАСКРИПТ</span></p>

          {showSecret && (
            <p className={styles.secretMessage}>
              СЕКР<span className={styles.glitch}>Е</span>ТНЫЙ ФЛА<span className={styles.shake}>Г</span> НА /flag ТРЕБУЕТСЯ ПЕ<span className={styles.rotate}>ЧЕ</span>НЬЕ
            </p>
          )}
        </div>

        <div className={styles.marquee}>
          <p>МИГАЮЩИЙ ТЕКСТ ВЫЗЫВАЕТ ПРИВЫКАНИЕ * СЛЕДУЮЩИЙ РЕШАЕТ * JS ЗАХВАТЫВАЕТ МИР * РАСТПОБЕДА БЛИЗКО * 1905 * 1905 * </p>
        </div>

        <div className={styles.images}>
          <div className={styles.spinningImage} style={{ transform: `rotate(${rotation}deg)` }}></div>
          <div className={styles.bouncingImage}></div>
          <div className={styles.pulsatingImage}></div>
        </div>

        <div className={styles.scrollingText}>
          <div>РАСТПОБЕДА</div>
          <div>СЛЕДУЮЩИЙ</div>
          <div>JS</div>
          <div>1905</div>
          <div>МОЗГ.EXE</div>
        </div>

        <button
          className={styles.crazyButton}
          onClick={() => document.location.href="https://youtube.com/watch?v=dQw4w9WgXcQ"}
        >
          НАЖМИ ДЛЯ 1905% РАСТПОБЕДЫ
        </button>
      </div>
    </main>
  );
}