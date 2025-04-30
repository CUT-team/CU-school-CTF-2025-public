'use client';

import { useEffect, useState } from 'react';
import styles from './page.module.css';

export default function FlagPage() {
  const [revealed, setRevealed] = useState(false);
  const [glitchLevel, setGlitchLevel] = useState(0);
  const [rotation, setRotation] = useState(0);

  useEffect(() => {
    const glitchInterval = setInterval(() => {
      setGlitchLevel(prev => Math.min(prev + 1, 10));
    }, 200);

    const revealTimer = setTimeout(() => setRevealed(true), 3000);

    const rotationInterval = setInterval(() => {
      setRotation(prev => (prev + 2) % 360);
    }, 50);

    return () => {
      clearInterval(glitchInterval);
      clearTimeout(revealTimer);
      clearInterval(rotationInterval);
    };
  }, []);

  const handleGlitchClick = () => {
    setGlitchLevel(prev => Math.min(prev + 2, 10));
  };

  return (
    <div className={styles.container} data-glitch-level={glitchLevel}>
      <div className={styles.static}></div>
      <div className={styles.scanlines}></div>

      <h1 className={styles.title} style={{ transform: `skew(${Math.sin(Date.now() * 0.001) * 10}deg, ${Math.cos(Date.now() * 0.002) * 5}deg)` }}>
        СЕКРЕТНЫЙ <span className={styles.glitch}>ФЛАГ 1905</span>
      </h1>

      <div className={styles.warningBox}>
        <div className={styles.warningHeader}>⚠️ ВЫСОКИЙ УРОВЕНЬ ДОСТУПА ⚠️</div>
        <div className={styles.warningContent}>
          ЗАГРУЗКА СЕКРЕТНЫХ ДАННЫХ...
          <div className={styles.loadingBar}>
            <div className={styles.loadingProgress} style={{ width: `${revealed ? '100%' : `${glitchLevel * 10}%`}` }}></div>
          </div>
        </div>
      </div>

      {!revealed ? (
        <div className={styles.loading}>
          <div className={styles.loadingText}>РАСШИФРОВКА ФЛАГА...</div>
          <div className={styles.spinner} style={{ transform: `rotate(${rotation}deg)` }}></div>
        </div>
      ) : (
        <div className={styles.flagContainer} onClick={handleGlitchClick}>
          <div className={styles.secretBox}>
            <div className={styles.secretHeader}>ДАННЫЕ РАСШИФРОВАНЫ</div>
            <p className={styles.flag}>{"cuctf{m1ddl3w4r3_p0b3d4_1905_n3x7_js_br41nr0t_fl4g_1337}"}</p>
          </div>

          <div className={styles.dizzyCube}>
            <div className={styles.cubeFace} style={{ transform: `rotateY(${rotation}deg) rotateX(${rotation / 2}deg)` }}>1905</div>
            <div className={styles.cubeFace} style={{ transform: `rotateY(${rotation + 90}deg) rotateX(${rotation / 2}deg)` }}>РАСТП</div>
            <div className={styles.cubeFace} style={{ transform: `rotateY(${rotation + 180}deg) rotateX(${rotation / 2}deg)` }}>ОБЕДА</div>
            <div className={styles.cubeFace} style={{ transform: `rotateY(${rotation + 270}deg) rotateX(${rotation / 2}deg)` }}>ФЛАГ</div>
          </div>
        </div>
      )}

      <div className={styles.terminalOutput}>
        <div>Доступ получен: root@brain-rot-1905</div>
        <div>Расшифровка: ████████████████ 100%</div>
        <div>Статус: СЛЕДУЮЩИЙ ЖС ПОБЕДА АКТИВИРОВАНА</div>
        <div className={styles.blinkText}>СЛЕДУЮЩИЙ JS ЗАГРУЖЕН В МОЗГ</div>
      </div>
    </div>
  );
}