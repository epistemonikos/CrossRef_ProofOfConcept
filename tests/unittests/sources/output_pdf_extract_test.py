result = ['NIST has recommended such a transition since 2010 [4]. We DHE', 'recommend that clients raise the minimum group size to 2048 bits as soon as server configurations allow. Server opera-', 'tors should move to 2048-bit or larger groups to facilitate this', 'transition. Precomputation for a 2048-bit non-trapdoored 9', 'group is around 10 times harder than for a 1024-bit group,', 'so 2048-bit Diffie-Hellman will remain secure barring a major', 'algorithmic improvement. For implementa- Avoid fixed-prime 1024-bit groups.', 'tions that must continue to use or support 1024-bit groups', 'for compatibility reasons, generating fresh groups may help', 'mitigate some of the damage caused by NFS-style precom-', 'putation for very common fixed groups. However, we note', 'that it is possible to create trapdoored primes [20, 44] that', 'are computationally difficult to detect. At minimum, clients', "should check that servers' parameters use safe primes or a verifiable generation process, such as that proposed in FIPS 186 [38]. Ideally, the process for generating and validating", 'parameters in TLS should be standardized so as to thwart', 'the risk of trapdoors. Our downgrade', "Don't deliberately weaken crypto.", 'attack on export-grade 512-bit Diffie-Hellman groups in TLS', 'illustrates the fragility of cryptographic "front doors". Al- DHE_EXPORT', 'though the key sizes originally used in were', 'intended to be tractable only to NSA, two decades of algo-', 'rithmic and computational improvements have significantly', 'lowered the bar to attacks on such key sizes. Despite the', 'eventual relaxation of crypto export restrictions and subse- DHE_EXPORT', 'quent attempts to remove support for , the', 'technical debt induced by the additional complexity has left', 'implementations vulnerable for decades. Like FREAK [7],', 'our attacks warn of the long-term debilitating effects of', 'deliberately weakening cryptography.', '6. DISCLOSURE AND RESPONSE We notified major client and server developers about', 'the vulnerabilities discussed in this paper before we made', 'our findings public. Prior to our work, Internet Explorer,', 'Chrome, Firefox, and Opera all accepted 512-bit primes, whereas Safari allowed groups as small as 16 bits. As a', 'result of our disclosures, Internet Explorer [37], Firefox, and DHE', 'Chrome are transitioning the minimum size of the groups', 'they accept to 1024 bits, and OpenSSL and Safari are ex-', 'pected to follow suit. On the server side, we notified Apache,', 'Oracle, IBM, Cisco, and various hosting providers. Aka-', 'mai has removed all support for export ciphersuites. Many TLS developers plan to support a new extension that allows', 'clients and servers to negotiate a few well-known groups of 2048-bits and higher and to gracefully reject weak ones [19].', '7. CONCLUSION Diffie-Hellman key exchange is a cornerstone of applied', 'cryptography, but we find that, as used in practice, it is often', 'less secure than widely believed. The problems stem from', 'the fact that the number field sieve for discrete log allows an', 'attacker to perform a single precomputation that depends', 'only on the group, after which computing individual logs in', 'that group has a far lower cost. Although this fact is well', "known to cryptographers, it apparently has not been widely understood by system builders. Likewise, many cryptogra- phers did not appreciate that the security of a large fraction of Internet communication depends on Diffie-Hellman key exchanges that use a few small, widely shared groups. A key lesson from this state of affairs is that cryptogra- phers and creators of practical systems need to work together more effectively. System builders should take responsibility for being aware of applicable cryptanalytic attacks. Cryp- tographers, for their part, should involve themselves in how crypto is actually being applied, such as through engagement with standards efforts and software review. Bridging the per- ilous gap that separates these communities will be essential for keeping future systems secure. Acknowledgments The authors wish to thank Michael Bailey, Daniel Bernstein, Ron Dreslinski, Tanja Lange, Adam Langley, Kenny Paterson, Andrei Popov, Ivan Ristic, Edward Snowden, Brian Smith, Martin Thomson, and Eric Rescorla. This material is based in part upon work supported by the U.S. National Science Foundation under contracts CNS-1345254, CNS-1409505, CNS-1518741, and EFRI-1441209, by the Office of Naval Research under contract N00014-11-1-0470, by the ERC Starting Grant 259639 (CRYSP), by the French ANR re- search grant ANR-12-BS02-001-01, by the NSF Graduate Research Fellowship Program under grant DGE-1256260, by the Mozilla Foundation, by a gift from Supermicro, by the Google Ph.D. Fellowship in Computer Security, by the Morris Wellman Faculty Development Assistant Professor- ship, and by an Alfred P. Sloan Foundation Research Fellow- ship. Some experiments were conducted using the Grid'5000 testbed, which is supported by INRIA, CNRS, RENATER, and several other universities and organizations; additional experiments used UCS hardware donated by Cisco.", 'S. Bai, C. Bouvier, A. Filbois, P. Gaudry, L. Imbert, A. Kruppa, F. Morain, E. Thomé, and P. Zimmermann. , an implementation of the number field sieve cado-nfs algorithm, 2014. Release 2.1.1.', 'R. Barbulescu. Algorithmes de logarithmes discrets dans les corps finis. PhD thesis, Université de Lorraine, France, 2013.', 'R. Barbulescu, P. Gaudry, A. Joux, and E. Thomé. A heuristic quasi-polynomial algorithm for discrete logarithm in finite fields of small characteristic. In Eurocrypt, 2014.', 'E. Barker, W. Barker, W. Burr, W. Polk, and M. Smid. NIST Special Publication 800-57: Recommendation for Key Management, 2007.', 'D. J. Bernstein. How to find smooth parts of integers, 2004. http://cr.yp.to/factorization/smoothparts-20040510.pdf .', 'D. J. Bernstein and T. Lange. Batch NFS. In Selected Areas in Cryptography, 2014.', 'B. Beurdouche, K. Bhargavan, A. Delignat-Lavaud, C. Fournet, M. Kohlweiss, A. Pironti, P.-Y. Strub, and J. K. Zinzindohoue. A messy state of the union: Taming the composite state machines of TLS. In IEEE Symposium on Security and Privacy, 2015.', 'C. Bouvier, P. Gaudry, L. Imbert, H. Jeljeli, and E. Thomé. New record for discrete logarithm in a prime finite field of 180 decimal digits, 2014. http://caramel.loria.fr/p180.txt.', "R. Canetti and H. Krawczyk. Security analysis of IKE's signature-based key-exchange protocol. In Crypto, 2002.", 'A. Commeine and I. Semaev. An algorithm to solve the discrete logarithm problem with the number field sieve. In PKC, 2006.', 'D. Coppersmith. Solving linear equations over GF(2) via block Wiedemann algorithm. Math. Comp., 62(205), 1994.', 'R. Crandall and C. B. Pomerance. Prime Numbers: A Computational Perspective. Springer, 2001.', 'B. den Boer. Diffie-Hellman is as strong as discrete log for certain primes. In Crypto, 1988.', 'W. Diffie and M. E. Hellman. New directions in cryptography. IEEE Trans. Inform. Theory, 22(6):644-654, 1976.', 'Z. Durumeric, E. Wustrow, and J. A. Halderman. ZMap: Fast Internet-wide scanning and its security applications. In Usenix Security, 2013. M. Friedl, N. Provos, and W. Simpson. Diffie-Hellman group', 'exchange for the secure shell (SSH) transport layer protocol. RFC 4419, Mar. 2006.', 'W. Geiselmann, H. Kopfer, R. Steinwandt, and E. Tromer. Improved routing-based linear algebra for the number field sieve. In Information Technology: Coding and Computing, 2005.', 'W. Geiselmann and R. Steinwandt. Non-wafer-scale sieving hardware for the NFS: Another attempt to cope with 1024-bit. In Eurocrypt, 2007. D. Gillmor. Negotiated finite field Diffie-Hellman ephemeral', 'parameters for TLS. IETF Internet Draft, May 2015.', 'D. M. Gordon. Designing and detecting trapdoors for discrete log cryptosystems. In Crypto, 1992.', 'D. M. Gordon. Discrete logarithms in GF(p) using the number field sieve. SIAM J. Discrete Math., 6(1), 1993.', 'D. Harkins and D. Carrel. The Internet key exchange (IKE). RFC 2409, Nov. 1998.', 'T. Jager, K. G. Paterson, and J. Somorovsky. One bad apple: Backwards compatibility attacks on state-of-the-art cryptography. In NDSS, 2013.', 'A. Joux and R. Lercier. Improvements to the general number field sieve for discrete logarithms in prime fields. A comparison with the Gaussian integer method. Math. Comp., 72(242):953-967, 2003.', 'C. Kaufman, P. Hoffman, Y. Nir, P. Eronen, and T. Kivinen. Internet key exchange protocol version 2 (IKEv2). RFC 7296, Oct. 2014.', 'S. Kent. IP authentication header. RFC 4302, Dec. 2005.', 'S. Kent. IP encapsulating security payload (ESP). RFC 4303, Dec. 2005.', 'T. Kleinjung. Cofactorisation strategies for the number field sieve and an estimate for the sieving step for factoring 1024 bit integers, 2006. http://www.hyperelliptic.org/tanja/ SHARCS/talks06/thorsten.pdf .', 'T. Kleinjung, K. Aoki, J. Franke, A. K. Lenstra, E. Thomé, J. W. Bos, P. Gaudry, A. Kruppa, P. L. Montgomery, D. A. Osvik, H. te Riele, A. Timofeev, and P. Zimmermann. Factorization of a 768-bit RSA modulus. In Crypto, 2010.', 'A. Langley, N. Modadugu, and B. Moeller. Transport layer security (TLS) false start. IETF Internet Draft, 2010.', 'A. K. Lenstra and H. W. Lenstra, Jr., editors. The Development of the Number Field Sieve. Springer, 1993.', 'M. Lipacis. Semiconductors: Moore stress = structural industry shift. Technical report, Jefferies, 2012.', 'U. M. Maurer. Towards the equivalence of breaking the Diffie-Hellman protocol and computing discrete logarithms. In Crypto, 1994. U. M. Maurer and S. Wolf. Diffie-Hellman oracles. In Crypto,', '1996.', 'N. Mavrogiannopoulos, F. Vercauteren, V. Velichkov, and B. Preneel. A cross-protocol attack on the TLS protocol. In ACM CCS, pages 62-72, 2012. C. Meadows. Analysis of the Internet key exchange protocol', 'using the NRL protocol analyzer. In IEEE Symposium on Security and Privacy, 1999.', 'Microsoft Security Bulletin MS15-055. Vulnerability in Schannel could allow information disclosure, May 2015.', 'NIST. FIPS PUB 186-4: Digital signature standard, 2013.', 'Oak Ridge National Laboratory. Introducing Titan, 2012. https://www.olcf.ornl.gov/titan.', 'H. Orman. The Oakley key determination protocol. RFC 2412, Nov. 1998.', 'S. C. Pohlig and M. E. Hellman. An improved algorithm for computing logarithms over GF(p) and its cryptographic significance (corresp.). Trans. Inform. Theory, 24(1), 1978.', 'J. M. Pollard. A Monte Carlo method for factorization. BIT Numerical Mathematics, 15(3):331-334, 1975.', 'O. Schirokauer. Virtual logarithms. J. Algorithms, 57(2):140-147, 2005.', 'I. A. Semaev. Special prime numbers and discrete logs in finite prime fields. Math. Comp., 71(237):363-377, 2002.', "D. Shanks. Class number, a theory of factorization, and genera. In Proc. Sympos. Pure Math., volume 20. 1971. Spiegel Staff. Prying eyes: Inside the NSA's war on Internet", 'security. Der Spiegel, Dec 2014. http://www.spiegel.de/international/germany/ inside-the-nsa-s-war-on-internet-security-a-1010361.html.', 'W. Stein et al. Sage Mathematics Software (Version 6.5). The Sage Development Team, 2015. http://www.sagemath.org.', 'stud: The scalable TLS unwrapping daemon, 2012. https://github.com/bumptech/stud/blob/ 19a7f19686bcdbd689c6fbea31f68a276e62d886/stud.c#L593.', 'E. Thomé. Subquadratic computation of vector generating polynomials and improvement of the block Wiedemann algorithm. J. Symbolic Comput., 33(5):757-775, 2002.', 'P. C. Van Oorschot and M. J. Wiener. Parallel collision search with application to hash functions and discrete logarithms. In ACM CCS, 1994.', 'P. C. Van Oorschot and M. J. Wiener. On Diffie-Hellman key agreement with short exponents. In Eurocrypt, 1996.', 'D. Wagner and B. Schneier. Analysis of the SSL 3.0 protocol. In 2nd Usenix Workshop on Electronic Commerce, 1996.', 'J. Wagnon. SSL profiles part 5: SSL options, 2013. https:// devcentral.f5.com/articles/ssl- profiles-part-5-ssl- options.', 'P. Zimmermann et al. GMP-ECM, 2012. https://gforge.inria.fr/projects/ecm.', 'APEX active/passive exfiltration. Media leak, Aug. 2009. http://www.spiegel.de/media/media-35671.pdf .', 'Fielded capability: End-to-end VPN SPIN 9 design review. Media leak. http://www.spiegel.de/media/media-35529.pdf .', 'FY 2013 congressional budget justification. Media leak. http://cryptome.org/2013/08/spy-budget-fy13.pdf .', 'GALLANTWAVE@scale. Media leak. http://www.spiegel.de/media/media-35514.pdf .', 'Innov8 experiment profile. Media leak. http://www.spiegel.de/media/media-35509.pdf .', 'Intro to the VPN exploitation process. Media leak, Sept. 2010. http://www.spiegel.de/media/media-35515.pdf .', 'LONGHAUL - WikiInfo. Media leak. http://www.spiegel.de/media/media-35533.pdf .', 'POISONNUT - WikiInfo. Media leak. http://www.spiegel.de/media/media-35519.pdf .', 'SIGINT strategy. Media leak. http://www.nytimes.com/interactive/2013/11/23/us/ politics/23nsa-sigint-strategy-document.html.', 'SPIN 15 VPN story. Media leak. http://www.spiegel.de/media/media-35522.pdf .', 'TURMOIL/APEX/APEX high level description document. Media leak. http://www.spiegel.de/media/media-35513.pdf .', 'TURMOIL IPsec VPN sessionization. Media leak, Aug. 2009. http://www.spiegel.de/media/media-35528.pdf .', 'TURMOIL VPN processing. Media leak, Oct. 2009. http://www.spiegel.de/media/media-35526.pdf .', 'VALIANTSURF (VS): Capability levels. Media leak. http://www.spiegel.de/media/media-35517.pdf .', 'VALIANTSURF - WikiInfo. Media leak. http://www.spiegel.de/media/media-35527.pdf .', 'VPN SigDev basics. Media leak. http://www.spiegel.de/media/media-35520.pdf .', 'What your mother never told you about SIGDEV analysis. Media leak. http://www.spiegel.de/media/media-35551.pdf .']