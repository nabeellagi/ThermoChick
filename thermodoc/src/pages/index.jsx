import Layout from '@theme/Layout';
import styles from './index.module.css';
import { useEffect, useRef } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import './index.module.css'

gsap.registerPlugin(ScrollTrigger);

function HomepageHeader() {
  return (
    <header>
      <link rel="preconnect" href="https://fonts.googleapis.com" />
      <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="true" />
      <link
        href="https://fonts.googleapis.com/css2?family=Familjen+Grotesk:wght@400..700&family=Fredoka:wght@300..700&family=Inter:wght@100..900&display=swap"
        rel="stylesheet"
      />
    </header>
  );
}

export default function Home() {
  const card1Ref = useRef(null);
  const card2Ref = useRef(null);
  const card3Ref = useRef(null);

  const suhuRef = useRef(null);
  const terangRef = useRef(null);

  const section1Ref = useRef(null);
  const section2Ref = useRef(null);
  const section3Ref = useRef(null);

  useEffect(() => {
    const bounceConfig = {
      y: -20,
      duration: 2,
      ease: "elastic.inOut(1.2,0.4)",
      repeat: -1,
      yoyo: true,
      delay: 0.2,
    };

    gsap.to(card1Ref.current, bounceConfig);
    gsap.to(card2Ref.current, { ...bounceConfig, delay: 0.6 });
    gsap.to(card3Ref.current, { ...bounceConfig, delay: 0.9 });

    const animateWords = (ref) => {
      if (!ref.current) return;

      const span = ref.current.querySelector('.text');
      const text = span.textContent;
      span.innerHTML = text
        .split('')
        .map(char => `<span class="word-char" style="display:inline-block">${char}</span>`)
        .join('');

      const splitChars = ref.current.querySelectorAll('.word-char');

      gsap.from(splitChars, {
        y: -100,
        opacity: 0,
        rotation: () => gsap.utils.random(-80, 80),
        duration: 1.5,
        ease: 'back',
        stagger: 0.15,
        onComplete: () => {
          gsap.to(splitChars, {
            y: '-=10',
            repeat: -1,
            yoyo: true,
            ease: "back.out(5)",
            duration: 0.5,
            stagger: {
              each: 0.1,
              repeat: -1,
              yoyo: true,
            },
          });
        }
      });
    };

    animateWords(suhuRef);
    animateWords(terangRef);

    // Section scroll animations
    [section1Ref, section2Ref, section3Ref].forEach((ref, i) => {
      if (!ref.current) return;
      gsap.from(ref.current, {
        opacity: 0,
        y: 100,
        duration: 1,
        ease: 'power2.out',
        scrollTrigger: {
          trigger: ref.current,
          start: 'top 85%',
          toggleActions: 'play none none none',
        },
      });
    });

  }, []);

  return (
    <Layout title={`ThermoChick Documentations`} description="Description will go into a meta tag in <head />">
      <HomepageHeader />

      <div
        style={{
          fontFamily: 'Fredoka, sans-serif',
          textAlign: 'center',
          padding: '50px 20px',
        }}
      >
        <h1
          style={{
            fontSize: '80px',
            fontWeight: '700',
            lineHeight: '1.2',
            position: 'relative',
            display: 'inline-block',
            textAlign: 'center',
          }}
        >
          Cerdas Pantau{' '}
          <span
            ref={suhuRef}
            style={{
              position: 'relative',
              display: 'inline-block',
              color: '#9C4FE2',
              fontFamily: 'Fredoka',
            }}
          >
            <span className="text">Suhu</span>
            <svg
              viewBox="0 0 100 10"
              preserveAspectRatio="none"
              style={{
                position: 'absolute',
                bottom: '-9px',
                left: '0',
                width: '100%',
                height: '12px',
              }}
            >
              <path d="M2 7 C 20 0, 80 14, 98 7" stroke="#E5C8FF" strokeWidth="4" fill="none" />
            </svg>
          </span>
          <br />
          <span
            ref={terangRef}
            style={{
              position: 'relative',
              display: 'inline-block',
              color: '#FFA500',
              fontFamily: 'Fredoka',
            }}
          >
            <span className="text">Terang</span>
            <svg
              viewBox="0 0 100 10"
              preserveAspectRatio="none"
              style={{
                position: 'absolute',
                bottom: '-6px',
                left: '0',
                width: '100%',
                height: '12px',
              }}
            >
              <path d="M2 7 C 20 0, 80 14, 98 7" stroke="#FFA500" strokeWidth="4" fill="none" />
            </svg>
          </span>{' '}
          Bantu Tumbuh
        </h1>

        <p style={{ fontSize: '18px', marginTop: '10px', color: '#444', fontFamily: 'Inter' }}>
          Bersama mempelajari fitur ThermoFarm
          <br />
          Singkat. Cepat. Tepat.
        </p>

        <div
          style={{
            display: 'flex',
            justifyContent: 'center',
            gap: '20px',
            flexWrap: 'wrap',
            marginTop: '40px',
          }}
        >
          <img
            ref={card1Ref}
            src="/img/frameui (1).svg"
            alt="Suhu Terkini"
            style={{
              width: '150px',
              maxWidth: '100%',
              height: 'auto',
              transform: 'rotate(-5deg)',
            }}
          />

          <img
            ref={card2Ref}
            src="/img/frameui (2).svg"
            alt="Prediksi Suhu"
            style={{
              width: '150px',
              maxWidth: '100%',
              height: 'auto',
              transform: 'rotate(0deg)',
            }}
          />

          <img
            ref={card3Ref}
            src="/img/frameui (3).svg"
            alt="Kondisi Lampu"
            style={{
              width: '150px',
              maxWidth: '100%',
              height: 'auto',
              transform: 'rotate(5deg)',
              borderRadius: '10px',
            }}
          />
        </div>

        {/* Section 1 */}
        <section ref={section1Ref}
          style={{
            padding: '60px 20px',
            textAlign: 'center',
            fontFamily: 'Inter, sans-serif',
            marginTop: 64,
          }}
        >
          <div style={{ maxWidth: '900px', margin: '0 auto' }}>
            <h2 style={{ fontSize: '48px', fontWeight: '700', marginBottom: '20px', color: '#222' }}>
              ThermoFarm Smart Farming
            </h2>
            <img
              src="/img/ex/dashboard.png"
              alt="Ilustrasi Fitur"
              style={{
                width: '50rem',
                height: 'auto',
                borderRadius: '12px',
                boxShadow: '0 4px 10px rgba(0,0,0,0.1)',
              }}
            />
            <p
              style={{
                fontSize: '20px',
                color: '#666',
                lineHeight: '1.6',
                marginBottom: '40px',
                textAlign: 'justify',
              }}
            >
              Gunakan ThermoFarm untuk memantau suhu dan kelembapan kandang, dilengkapi fitur prediksi dan automasi pencahayaan lampu!
            </p>
          </div>
        </section>

        {/* Section 2 */}
        <section ref={section2Ref}
          style={{
            padding: '60px 20px',
            textAlign: 'center',
            fontFamily: 'Inter, sans-serif',
            marginTop: 30,
          }}
        >
          <div style={{ maxWidth: '900px', margin: '0 auto' }}>
            <h2 style={{ fontSize: '48px', fontWeight: '700', marginBottom: '20px', color: '#222' }}>
              AI Integrated
            </h2>
            <img
              src="/img/ex/smart.png"
              alt="Ilustrasi AI"
              style={{
                width: '50rem',
                height: 'auto',
                borderRadius: '12px',
                boxShadow: '0 4px 10px rgba(0,0,0,0.1)',
              }}
            />
            <p
              style={{
                fontSize: '20px',
                color: '#666',
                lineHeight: '1.6',
                marginBottom: '40px',
                textAlign: 'justify',
              }}
            >
              Dilengkapi dengan fitur asisten AI dan prediksi suhu dan kelembaban! Gunakan sebagai alat penunjang, mitigasi, dan rise
            </p>
          </div>
        </section>

        {/* Section 3 - CTA */}
        <section ref={section3Ref}
          style={{
            padding: '60px 20px',
            textAlign: 'center',
            fontFamily: 'Inter, sans-serif',
            marginTop: 30,
          }}
        >
          <div style={{ maxWidth: '800px', margin: '0 auto' }}>
            <h2 style={{ fontSize: '44px', fontWeight: '700', color: '#3B0CA8', marginBottom: '20px' }}>
              📘 Pelajari Lebih Lanjut di ThermoDoc
            </h2>
            <p style={{ fontSize: '20px', color: '#555', marginBottom: '30px' }}>
              Jelajahi dokumentasi ThermoFarm: panduan lengkap, fitur, integrasi AI, prediksi cerdas, dan tips efisien dalam smart farming. Siap jadi peternak masa depan?
            </p>
            <a
              href="/docs/intro"
              style={{
                fontSize: '18px',
                padding: '14px 28px',
                borderRadius: '8px',
                textDecoration: 'none',
                fontWeight: '600',
                boxShadow: '0 4px 12px rgba(59,12,168,0.3)',
                transition: 'transform 0.2s ease-in-out',
              }}
              onMouseOver={e => (e.currentTarget.style.transform = 'scale(1.05)')}
              onMouseOut={e => (e.currentTarget.style.transform = 'scale(1)')}
            >
              📖 Buka ThermoDoc
            </a>
          </div>
        </section>
      </div>
    </Layout>
  );
}