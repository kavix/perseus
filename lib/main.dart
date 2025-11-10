import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'database_helper.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Enable immersive full-screen mode
  SystemChrome.setEnabledSystemUIMode(SystemUiMode.immersive);
  
  // Set status bar and navigation bar to transparent
  SystemChrome.setSystemUIOverlayStyle(
    const SystemUiOverlayStyle(
      statusBarColor: Colors.transparent,
      systemNavigationBarColor: Colors.transparent,
    ),
  );
  
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'MEDUSA CTF',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF39FF14), // Neon green
          brightness: Brightness.dark,
        ),
        useMaterial3: true,
      ),
      home: const LoginPage(),
    );
  }
}

// ============================================================================
// LOGIN PAGE
// ============================================================================

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> with TickerProviderStateMixin {
  final _formKey = GlobalKey<FormState>();
  final _usernameController = TextEditingController();
  final _passwordController = TextEditingController();
  
  bool _isLoading = false;
  bool _showError = false;
  
  late AnimationController _shakeController;
  late AnimationController _glowController;
  late Animation<double> _shakeAnimation;
  late Animation<double> _glowAnimation;

  @override
  void initState() {
    super.initState();
    
    // Shake animation for error
    _shakeController = AnimationController(
      duration: const Duration(milliseconds: 500),
      vsync: this,
    );
    _shakeAnimation = Tween<double>(begin: 0, end: 10).animate(
      CurvedAnimation(parent: _shakeController, curve: Curves.elasticIn),
    );
    
    // Glow animation for logo
    _glowController = AnimationController(
      duration: const Duration(seconds: 2),
      vsync: this,
    )..repeat(reverse: true);
    _glowAnimation = Tween<double>(begin: 0.3, end: 1.0).animate(
      CurvedAnimation(parent: _glowController, curve: Curves.easeInOut),
    );
  }

  @override
  void dispose() {
    _usernameController.dispose();
    _passwordController.dispose();
    _shakeController.dispose();
    _glowController.dispose();
    super.dispose();
  }

  Future<void> _handleSubmit() async {
    if (!_formKey.currentState!.validate()) {
      _shakeController.forward(from: 0);
      return;
    }

    setState(() {
      _isLoading = true;
      _showError = false;
    });

    try {
      final result = await DatabaseHelper.instance.verifyCredentials(
        _usernameController.text,
        _passwordController.text,
      );

      if (result != null) {
        // Success - navigate to flag page
        HapticFeedback.heavyImpact();
        
        if (mounted) {
          Navigator.of(context).push(
            PageRouteBuilder(
              pageBuilder: (context, animation, secondaryAnimation) => 
                FlagPage(flag: result['flag']),
              transitionsBuilder: (context, animation, secondaryAnimation, child) {
                const begin = Offset(1.0, 0.0);
                const end = Offset.zero;
                const curve = Curves.easeInOut;

                var tween = Tween(begin: begin, end: end).chain(
                  CurveTween(curve: curve),
                );
                var offsetAnimation = animation.drive(tween);

                return SlideTransition(
                  position: offsetAnimation,
                  child: FadeTransition(
                    opacity: animation,
                    child: child,
                  ),
                );
              },
              transitionDuration: const Duration(milliseconds: 500),
            ),
          );
        }
      } else {
        // Error - show error message
        HapticFeedback.vibrate();
        setState(() {
          _showError = true;
        });
        _shakeController.forward(from: 0);
      }
    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [
              Color(0xFF0F172A),
              Color(0xFF1E293B),
              Color(0xFF334155),
            ],
          ),
        ),
        child: SafeArea(
          child: Center(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(24.0),
              child: AnimatedBuilder(
                animation: _shakeAnimation,
                builder: (context, child) {
                  return Transform.translate(
                    offset: Offset(_shakeAnimation.value, 0),
                    child: child,
                  );
                },
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    // Logo with glow effect
                    AnimatedBuilder(
                      animation: _glowAnimation,
                      builder: (context, child) {
                        return Container(
                          width: 150,
                          height: 150,
                          decoration: BoxDecoration(
                            shape: BoxShape.circle,
                            boxShadow: [
                              BoxShadow(
                                color: const Color(0xFF39FF14).withOpacity(_glowAnimation.value * 0.5),
                                blurRadius: 30,
                                spreadRadius: 10,
                              ),
                            ],
                          ),
                          child: ClipOval(
                            child: Container(
                              color: Colors.black12,
                              padding: const EdgeInsets.all(20),
                              child: Image.asset(
                                'assets/images/logo.png',
                                fit: BoxFit.contain,
                              ),
                            ),
                          ),
                        );
                      },
                    ),
                    
                    const SizedBox(height: 32),
                    
                    // Title
                    const Text(
                      'The Gorgon\'s Challenge',
                      style: TextStyle(
                        fontSize: 28,
                        fontWeight: FontWeight.bold,
                        color: Color(0xFF39FF14),
                        letterSpacing: 1.5,
                      ),
                      textAlign: TextAlign.center,
                    ),
                    
                    const SizedBox(height: 16),
                    
                    // Mythology text
                    const Text(
                      'In ancient myth, Medusa\'s gaze turned warriors to stone.\nOnly the worthy may pass...',
                      style: TextStyle(
                        fontSize: 14,
                        color: Colors.white70,
                        height: 1.5,
                      ),
                      textAlign: TextAlign.center,
                    ),
                    
                    const SizedBox(height: 8),
                    
                    // Read the Legend link
                    TextButton(
                      onPressed: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(builder: (context) => const StoryPage()),
                        );
                      },
                      child: const Text(
                        'Read the Legend',
                        style: TextStyle(
                          color: Color(0xFF39FF14),
                          decoration: TextDecoration.underline,
                        ),
                      ),
                    ),
                    
                    const SizedBox(height: 32),
                    
                    // Login Form
                    Form(
                      key: _formKey,
                      child: Column(
                        children: [
                          // Username field
                          TextFormField(
                            controller: _usernameController,
                            style: const TextStyle(color: Colors.white),
                            decoration: InputDecoration(
                              labelText: 'Username',
                              labelStyle: const TextStyle(color: Color(0xFF39FF14)),
                              enabledBorder: OutlineInputBorder(
                                borderSide: const BorderSide(color: Color(0xFF39FF14)),
                                borderRadius: BorderRadius.circular(8),
                              ),
                              focusedBorder: OutlineInputBorder(
                                borderSide: const BorderSide(color: Color(0xFF39FF14), width: 2),
                                borderRadius: BorderRadius.circular(8),
                              ),
                              errorBorder: OutlineInputBorder(
                                borderSide: const BorderSide(color: Colors.red),
                                borderRadius: BorderRadius.circular(8),
                              ),
                              focusedErrorBorder: OutlineInputBorder(
                                borderSide: const BorderSide(color: Colors.red, width: 2),
                                borderRadius: BorderRadius.circular(8),
                              ),
                              prefixIcon: const Icon(Icons.person, color: Color(0xFF39FF14)),
                            ),
                            validator: (value) {
                              if (value == null || value.isEmpty) {
                                return 'Please enter username';
                              }
                              return null;
                            },
                          ),
                          
                          const SizedBox(height: 16),
                          
                          // Password field
                          TextFormField(
                            controller: _passwordController,
                            obscureText: true,
                            style: const TextStyle(color: Colors.white),
                            decoration: InputDecoration(
                              labelText: 'Password',
                              labelStyle: const TextStyle(color: Color(0xFF39FF14)),
                              enabledBorder: OutlineInputBorder(
                                borderSide: const BorderSide(color: Color(0xFF39FF14)),
                                borderRadius: BorderRadius.circular(8),
                              ),
                              focusedBorder: OutlineInputBorder(
                                borderSide: const BorderSide(color: Color(0xFF39FF14), width: 2),
                                borderRadius: BorderRadius.circular(8),
                              ),
                              errorBorder: OutlineInputBorder(
                                borderSide: const BorderSide(color: Colors.red),
                                borderRadius: BorderRadius.circular(8),
                              ),
                              focusedErrorBorder: OutlineInputBorder(
                                borderSide: const BorderSide(color: Colors.red, width: 2),
                                borderRadius: BorderRadius.circular(8),
                              ),
                              prefixIcon: const Icon(Icons.lock, color: Color(0xFF39FF14)),
                            ),
                            validator: (value) {
                              if (value == null || value.isEmpty) {
                                return 'Please enter password';
                              }
                              return null;
                            },
                          ),
                          
                          const SizedBox(height: 24),
                          
                          // Error message
                          AnimatedOpacity(
                            opacity: _showError ? 1.0 : 0.0,
                            duration: const Duration(milliseconds: 300),
                            child: Container(
                              padding: const EdgeInsets.all(12),
                              decoration: BoxDecoration(
                                color: Colors.red.withOpacity(0.2),
                                borderRadius: BorderRadius.circular(8),
                                border: Border.all(color: Colors.red),
                              ),
                              child: const Row(
                                children: [
                                  Icon(Icons.error, color: Colors.red),
                                  SizedBox(width: 8),
                                  Expanded(
                                    child: Text(
                                      'Invalid credentials. Access denied.',
                                      style: TextStyle(color: Colors.red),
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ),
                          
                          if (_showError) const SizedBox(height: 16),
                          
                          // Submit button
                          SizedBox(
                            width: double.infinity,
                            height: 56,
                            child: AnimatedContainer(
                              duration: const Duration(milliseconds: 300),
                              decoration: BoxDecoration(
                                gradient: LinearGradient(
                                  colors: _isLoading
                                      ? [Colors.grey, Colors.grey.shade800]
                                      : [const Color(0xFF39FF14), const Color(0xFF2ECC11)],
                                ),
                                borderRadius: BorderRadius.circular(8),
                                boxShadow: [
                                  BoxShadow(
                                    color: _isLoading 
                                        ? Colors.transparent 
                                        : const Color(0xFF39FF14).withOpacity(0.3),
                                    blurRadius: 10,
                                    spreadRadius: 2,
                                  ),
                                ],
                              ),
                              child: ElevatedButton(
                                onPressed: _isLoading ? null : _handleSubmit,
                                style: ElevatedButton.styleFrom(
                                  backgroundColor: Colors.transparent,
                                  shadowColor: Colors.transparent,
                                  shape: RoundedRectangleBorder(
                                    borderRadius: BorderRadius.circular(8),
                                  ),
                                ),
                                child: _isLoading
                                    ? const SizedBox(
                                        width: 24,
                                        height: 24,
                                        child: CircularProgressIndicator(
                                          color: Colors.white,
                                          strokeWidth: 2,
                                        ),
                                      )
                                    : const Text(
                                        'ACCESS SYSTEM',
                                        style: TextStyle(
                                          fontSize: 16,
                                          fontWeight: FontWeight.bold,
                                          color: Colors.black,
                                          letterSpacing: 1.2,
                                        ),
                                      ),
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}

// ============================================================================
// FLAG PAGE
// ============================================================================

class FlagPage extends StatefulWidget {
  final String flag;

  const FlagPage({super.key, required this.flag});

  @override
  State<FlagPage> createState() => _FlagPageState();
}

class _FlagPageState extends State<FlagPage> with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _scaleAnimation;
  late Animation<double> _fadeAnimation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(milliseconds: 800),
      vsync: this,
    );

    _scaleAnimation = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(parent: _controller, curve: Curves.elasticOut),
    );

    _fadeAnimation = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeIn),
    );

    _controller.forward();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [
              Color(0xFF0F172A),
              Color(0xFF1E293B),
              Color(0xFF334155),
            ],
          ),
        ),
        child: SafeArea(
          child: Center(
            child: Padding(
              padding: const EdgeInsets.all(24.0),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  // Success checkmark animation
                  ScaleTransition(
                    scale: _scaleAnimation,
                    child: Container(
                      width: 120,
                      height: 120,
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        color: const Color(0xFF39FF14).withOpacity(0.2),
                        boxShadow: [
                          BoxShadow(
                            color: const Color(0xFF39FF14).withOpacity(0.5),
                            blurRadius: 30,
                            spreadRadius: 10,
                          ),
                        ],
                      ),
                      child: const Icon(
                        Icons.check,
                        size: 80,
                        color: Color(0xFF39FF14),
                      ),
                    ),
                  ),

                  const SizedBox(height: 32),

                  FadeTransition(
                    opacity: _fadeAnimation,
                    child: Column(
                      children: [
                        const Text(
                          'Access Granted!',
                          style: TextStyle(
                            fontSize: 32,
                            fontWeight: FontWeight.bold,
                            color: Color(0xFF39FF14),
                            letterSpacing: 1.5,
                          ),
                        ),

                        const SizedBox(height: 16),

                        const Text(
                          'You have successfully bypassed the Gorgon\'s gaze',
                          style: TextStyle(
                            fontSize: 16,
                            color: Colors.white70,
                          ),
                          textAlign: TextAlign.center,
                        ),

                        const SizedBox(height: 32),

                        // Flag container
                        Container(
                          padding: const EdgeInsets.all(24),
                          decoration: BoxDecoration(
                            color: Colors.black.withOpacity(0.5),
                            borderRadius: BorderRadius.circular(12),
                            border: Border.all(
                              color: const Color(0xFF39FF14),
                              width: 2,
                            ),
                            boxShadow: [
                              BoxShadow(
                                color: const Color(0xFF39FF14).withOpacity(0.3),
                                blurRadius: 20,
                                spreadRadius: 2,
                              ),
                            ],
                          ),
                          child: Column(
                            children: [
                              const Text(
                                'YOUR FLAG:',
                                style: TextStyle(
                                  fontSize: 14,
                                  color: Color(0xFF39FF14),
                                  letterSpacing: 2,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                              const SizedBox(height: 16),
                              SelectableText(
                                widget.flag,
                                style: const TextStyle(
                                  fontSize: 20,
                                  fontFamily: 'Courier',
                                  color: Colors.white,
                                  fontWeight: FontWeight.bold,
                                ),
                                textAlign: TextAlign.center,
                              ),
                            ],
                          ),
                        ),

                        const SizedBox(height: 32),

                        // Back button
                        OutlinedButton.icon(
                          onPressed: () {
                            Navigator.of(context).pop();
                          },
                          icon: const Icon(Icons.arrow_back),
                          label: const Text('Return to Login'),
                          style: OutlinedButton.styleFrom(
                            foregroundColor: const Color(0xFF39FF14),
                            side: const BorderSide(color: Color(0xFF39FF14)),
                            padding: const EdgeInsets.symmetric(
                              horizontal: 24,
                              vertical: 12,
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}

// ============================================================================
// STORY PAGE
// ============================================================================

class StoryPage extends StatelessWidget {
  const StoryPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [
              Color(0xFF0F172A),
              Color(0xFF1E293B),
              Color(0xFF334155),
            ],
          ),
        ),
        child: SafeArea(
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(24.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Back button
                IconButton(
                  onPressed: () {
                    Navigator.of(context).pop();
                  },
                  icon: const Icon(Icons.arrow_back),
                  color: const Color(0xFF39FF14),
                ),

                const SizedBox(height: 16),

                // Title
                const Text(
                  'The Legend of Medusa',
                  style: TextStyle(
                    fontSize: 32,
                    fontWeight: FontWeight.bold,
                    color: Color(0xFF39FF14),
                    letterSpacing: 1.5,
                  ),
                ),

                const SizedBox(height: 24),

                // Story content
                const Text(
                  'In the ancient myths of Greece, Medusa was one of the three Gorgon sisters. '
                  'Once a beautiful maiden, she was transformed into a monster with living venomous '
                  'snakes in place of hair.\n\n'
                  'Her most fearsome power was her gaze - anyone who looked directly into her eyes '
                  'would be instantly turned to stone. Warriors and heroes from across the land '
                  'attempted to slay her, but all fell victim to her petrifying stare.\n\n'
                  'The hero Perseus succeeded where others failed. Using his polished shield as a '
                  'mirror, he avoided her direct gaze and struck her down, claiming her head as a '
                  'trophy. Even in death, Medusa\'s head retained its power to turn those who gazed '
                  'upon it to stone.\n\n'
                  'Like Perseus, you must use cleverness and skill to overcome the challenges before '
                  'you. The path to victory requires more than brute force - it demands wisdom, '
                  'insight, and the ability to see what others cannot.\n\n'
                  'Will you prove yourself worthy of passing the Gorgon\'s test?',
                  style: TextStyle(
                    fontSize: 16,
                    color: Colors.white70,
                    height: 1.8,
                  ),
                ),

                const SizedBox(height: 32),

                Center(
                  child: Container(
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      border: Border.all(color: Color(0xFF39FF14)),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: const Text(
                      'MEDUSA CTF 2.0\nAndroid Exploitation Challenge\nby kavix',
                      style: TextStyle(
                        fontSize: 14,
                        color: Color(0xFF39FF14),
                        fontWeight: FontWeight.bold,
                        letterSpacing: 1.2,
                      ),
                      textAlign: TextAlign.center,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
