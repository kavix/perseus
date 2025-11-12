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
        colorScheme: const ColorScheme(
          brightness: Brightness.dark,
          primary: Color(0xFF08CB00),
          onPrimary: Color(0xFF000000),
          secondary: Color(0xFF253900),
          onSecondary: Color(0xFFEEEEEE),
          error: Colors.red,
          onError: Color(0xFF000000),
          surface: Color(0xFF000000),
          onSurface: Color(0xFFEEEEEE),
        ),
        scaffoldBackgroundColor: const Color(0xFF000000),
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
  bool _obscurePassword = true;
  bool _canSubmit = false;
  
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

    // Enable/disable submit button based on inputs
    void updateCanSubmit() {
      final can = _usernameController.text.trim().isNotEmpty &&
          _passwordController.text.isNotEmpty;
      if (can != _canSubmit) {
        setState(() => _canSubmit = can);
      }
    }
    // Initial state and listeners
    _canSubmit = _usernameController.text.trim().isNotEmpty &&
        _passwordController.text.isNotEmpty;
    _usernameController.addListener(updateCanSubmit);
    _passwordController.addListener(updateCanSubmit);
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
              Color(0xFF000000),
              Color(0xFF253900),
              Color(0xFF000000),
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
                        return ConstrainedBox(
                          constraints: const BoxConstraints(maxWidth: 420),
                          child: Container(
                            height: 180,
                            decoration: BoxDecoration(
                              boxShadow: [
                                BoxShadow(
                                  color: const Color(0xFF08CB00).withValues(alpha: (_glowAnimation.value * 0.5).clamp(0,1)),
                                  blurRadius: 30,
                                  spreadRadius: 10,
                                ),
                              ],
                            ),
                            child: Padding(
                              padding: const EdgeInsets.all(20),
                              child: Image.asset(
                                'assets/images/logo.png',
                                fit: BoxFit.contain,
                                semanticLabel: 'Challenge logo',
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
                        color: Color(0xFF08CB00),
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
                        color: Color(0xFFEEEEEE),
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
                          color: Color(0xFF08CB00),
                          decoration: TextDecoration.underline,
                        ),
                      ),
                    ),
                    
                    const SizedBox(height: 32),
                    
                    // Login Form
                    Form(
                      autovalidateMode: AutovalidateMode.onUserInteraction,
                      key: _formKey,
                      child: Column(
                        children: [
                          // Username field
                          TextFormField(
                            controller: _usernameController,
                            textInputAction: TextInputAction.next,
                            style: const TextStyle(color: Color(0xFFEEEEEE)),
                            decoration: InputDecoration(
                              labelText: 'Divine Name',
                              hintText: 'Enter your immortal name...',
                              hintStyle: const TextStyle(color: Colors.white30),
                              labelStyle: const TextStyle(color: Color(0xFF08CB00)),
                              enabledBorder: OutlineInputBorder(
                                borderSide: const BorderSide(color: Color(0xFF08CB00)),
                                borderRadius: BorderRadius.circular(8),
                              ),
                              focusedBorder: OutlineInputBorder(
                                borderSide: const BorderSide(color: Color(0xFF08CB00), width: 2),
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
                              prefixIcon: const Icon(Icons.person, color: Color(0xFF08CB00)),
                            ),
                            autofillHints: const [AutofillHints.username],
                            onFieldSubmitted: (_) => FocusScope.of(context).nextFocus(),
                            validator: (value) {
                              if (value == null || value.isEmpty) {
                                return 'The gods require your name';
                              }
                              return null;
                            },
                          ),
                          
                          const SizedBox(height: 16),
                          
                          // Password field
                          TextFormField(
                            controller: _passwordController,
                            obscureText: _obscurePassword,
                            textInputAction: TextInputAction.done,
                            style: const TextStyle(color: Color(0xFFEEEEEE)),
                            decoration: InputDecoration(
                              labelText: 'Sacred Key',
                              hintText: 'Speak your secret words...',
                              hintStyle: const TextStyle(color: Colors.white30),
                              labelStyle: const TextStyle(color: Color(0xFF08CB00)),
                              enabledBorder: OutlineInputBorder(
                                borderSide: const BorderSide(color: Color(0xFF08CB00)),
                                borderRadius: BorderRadius.circular(8),
                              ),
                              focusedBorder: OutlineInputBorder(
                                borderSide: const BorderSide(color: Color(0xFF08CB00), width: 2),
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
                              prefixIcon: const Icon(Icons.lock, color: Color(0xFF08CB00)),
                              suffixIcon: IconButton(
                                onPressed: () => setState(() => _obscurePassword = !_obscurePassword),
                                icon: Icon(
                                  _obscurePassword ? Icons.visibility : Icons.visibility_off,
                                  color: const Color(0xFF08CB00),
                                ),
                                tooltip: _obscurePassword ? 'Show key' : 'Hide key',
                              ),
                            ),
                            autofillHints: const [AutofillHints.password],
                            onFieldSubmitted: (_) {
                              if (!_isLoading && _canSubmit) _handleSubmit();
                            },
                            validator: (value) {
                              if (value == null || value.isEmpty) {
                                return 'The sacred key must not be empty';
                              }
                              return null;
                            },
                          ),

                          // Forgot key link
                          Align(
                            alignment: Alignment.centerRight,
                            child: TextButton(
                              onPressed: () {
                                showDialog(
                                  context: context,
                                  builder: (context) => AlertDialog(
                                    title: const Text('Forgot the Sacred Key?'),
                                    content: const Text(
                                      'Seek clues in Zeus\'s domain: sacred texts, configuration scrolls, or artifacts left behind.',
                                    ),
                                    actions: [
                                      TextButton(
                                        onPressed: () => Navigator.of(context).pop(),
                                        child: const Text('Got it'),
                                      ),
                                    ],
                                  ),
                                );
                              },
                              child: const Text(
                                'Forgot the Sacred Key?',
                                style: TextStyle(color: Color(0xFF08CB00)),
                              ),
                            ),
                          ),
                          
                          const SizedBox(height: 24),
                          
                          // Error message
                          AnimatedOpacity(
                            opacity: _showError ? 1.0 : 0.0,
                            duration: const Duration(milliseconds: 300),
                            child: Container(
                              padding: const EdgeInsets.all(12),
                              decoration: BoxDecoration(
                                color: const Color.fromRGBO(255, 0, 0, 0.2),
                                borderRadius: BorderRadius.circular(8),
                                border: Border.all(color: Colors.red),
                              ),
                              child: const Row(
                                children: [
                                  Icon(Icons.error, color: Colors.red),
                                  SizedBox(width: 8),
                                  Expanded(
                                    child: Text(
                                      'Medusa\'s gaze rejects false mortals...',
                                      style: TextStyle(
                                        color: Colors.red,
                                        fontStyle: FontStyle.italic,
                                      ),
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
                                      : [const Color(0xFF08CB00), const Color(0xFF253900)],
                                ),
                                borderRadius: BorderRadius.circular(8),
                                boxShadow: [
                                  BoxShadow(
                                    color: _isLoading 
                                        ? Colors.transparent 
                                        : const Color(0xFF08CB00).withValues(alpha: 0.3),
                                    blurRadius: 10,
                                    spreadRadius: 2,
                                  ),
                                ],
                              ),
                              child: ElevatedButton(
                                onPressed: _isLoading || !_canSubmit ? null : _handleSubmit,
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
                                          color: Color(0xFFEEEEEE),
                                          strokeWidth: 2,
                                        ),
                                      )
                                    : const Text(
                                        'FACE THE GORGON',
                                        style: TextStyle(
                                          fontSize: 16,
                                          fontWeight: FontWeight.bold,
                                          color: Color(0xFF000000),
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
  late bool _isRealFlag;

  @override
  void initState() {
    super.initState();
    
    // Check if this is the real decrypted flag (starts with MEDUSA{)
    // vs encrypted/fake flag (starts with FakeFlag{)
    _isRealFlag = widget.flag.startsWith('MEDUSA{');
    
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
              Color(0xFF000000),
              Color(0xFF253900),
              Color(0xFF000000),
            ],
          ),
        ),
        child: SafeArea(
          child: LayoutBuilder(
            builder: (context, constraints) {
              return SingleChildScrollView(
                padding: const EdgeInsets.all(24.0),
                child: ConstrainedBox(
                  constraints: BoxConstraints(minHeight: constraints.maxHeight),
                  child: Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        ScaleTransition(
                          scale: _scaleAnimation,
                          child: Container(
                            width: 120,
                            height: 120,
                            decoration: BoxDecoration(
                              shape: BoxShape.circle,
                              color: _isRealFlag 
                                  ? const Color(0xFF08CB00).withValues(alpha: 0.25)
                                  : Colors.orange.withValues(alpha: 0.25),
                              boxShadow: [
                                BoxShadow(
                                  color: _isRealFlag
                                      ? const Color(0xFF08CB00).withValues(alpha: 0.55)
                                      : Colors.orange.withValues(alpha: 0.55),
                                  blurRadius: 30,
                                  spreadRadius: 10,
                                ),
                              ],
                            ),
                            child: Icon(
                              _isRealFlag ? Icons.check : Icons.warning,
                              size: 80,
                              color: _isRealFlag ? const Color(0xFF08CB00) : Colors.orange,
                            ),
                          ),
                        ),
                        const SizedBox(height: 32),
                        FadeTransition(
                          opacity: _fadeAnimation,
                          child: Column(
                            children: [
                              Text(
                                _isRealFlag 
                                    ? 'The Gorgon\'s Secret Revealed!'
                                    : 'Encrypted Mystery...',
                                style: TextStyle(
                                  fontSize: 32,
                                  fontWeight: FontWeight.bold,
                                  color: _isRealFlag ? const Color(0xFF08CB00) : Colors.orange,
                                  letterSpacing: 1.5,
                                ),
                                textAlign: TextAlign.center,
                              ),
                              const SizedBox(height: 16),
                              Text(
                                _isRealFlag
                                    ? 'The immortals have spoken. You are worthy...'
                                    : 'The secrets remain veiled. Only the true key-holder may unveil them...',
                                style: const TextStyle(
                                  fontSize: 16,
                                  color: Color(0xFFEEEEEE),
                                  fontStyle: FontStyle.italic,
                                ),
                                textAlign: TextAlign.center,
                              ),
                              const SizedBox(height: 32),
                              Container(
                                padding: const EdgeInsets.all(24),
                                decoration: BoxDecoration(
                                  color: const Color.fromRGBO(0, 0, 0, 0.5),
                                  borderRadius: BorderRadius.circular(12),
                                  border: Border.all(
                                    color: _isRealFlag ? const Color(0xFF08CB00) : Colors.orange,
                                    width: 2,
                                  ),
                                  boxShadow: [
                                    BoxShadow(
                                      color: _isRealFlag
                                          ? const Color(0xFF08CB00).withValues(alpha: 0.3)
                                          : Colors.orange.withValues(alpha: 0.3),
                                      blurRadius: 20,
                                      spreadRadius: 2,
                                    ),
                                  ],
                                ),
                                child: Column(
                                  children: [
                                    Text(
                                      _isRealFlag ? 'DIVINE DECREE:' : 'ENCRYPTED DATA:',
                                      style: TextStyle(
                                        fontSize: 14,
                                        color: _isRealFlag ? const Color(0xFF08CB00) : Colors.orange,
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
                                        color: Color(0xFFEEEEEE),
                                        fontWeight: FontWeight.bold,
                                      ),
                                      textAlign: TextAlign.center,
                                    ),
                                    const SizedBox(height: 12),
                                    OutlinedButton.icon(
                                      onPressed: () {
                                        Clipboard.setData(ClipboardData(text: widget.flag));
                                        ScaffoldMessenger.of(context).showSnackBar(
                                          SnackBar(
                                            content: Text(_isRealFlag 
                                                ? 'Flag copied to clipboard'
                                                : 'Encrypted data copied to clipboard'),
                                            duration: const Duration(seconds: 2),
                                          ),
                                        );
                                      },
                                      icon: const Icon(Icons.copy),
                                      label: Text(_isRealFlag ? 'Copy Flag' : 'Copy Data'),
                                      style: OutlinedButton.styleFrom(
                                        foregroundColor: _isRealFlag ? const Color(0xFF08CB00) : Colors.orange,
                                        side: BorderSide(color: _isRealFlag ? const Color(0xFF08CB00) : Colors.orange),
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                              
                              // Show MT6.jpg image only when real flag is decrypted
                              if (_isRealFlag) ...[
                                const SizedBox(height: 32),
                                Container(
                                  padding: const EdgeInsets.all(16),
                                  decoration: BoxDecoration(
                                    color: const Color.fromRGBO(0, 0, 0, 0.5),
                                    borderRadius: BorderRadius.circular(12),
                                    border: Border.all(
                                      color: const Color(0xFF08CB00),
                                      width: 2,
                                    ),
                                    boxShadow: [
                                      BoxShadow(
                                        color: const Color(0xFF08CB00).withValues(alpha: 0.3),
                                        blurRadius: 20,
                                        spreadRadius: 2,
                                      ),
                                    ],
                                  ),
                                  child: Column(
                                    children: [
                                      const Text(
                                        'Look sharp. Hack harder.',
                                        style: TextStyle(
                                          fontSize: 14,
                                          color: Color(0xFF08CB00),
                                          letterSpacing: 2,
                                          fontWeight: FontWeight.bold,
                                        ),
                                      ),
                                      const SizedBox(height: 16),
                                      ClipRRect(
                                        borderRadius: BorderRadius.circular(8),
                                        child: Image.asset(
                                          'assets/images/MT6.jpg',
                                          fit: BoxFit.contain,
                                          semanticLabel: 'Divine revelation from Zeus',
                                          errorBuilder: (context, error, stackTrace) {
                                            return Container(
                                              padding: const EdgeInsets.all(20),
                                              child: const Text(
                                                'Image could not be loaded',
                                                style: TextStyle(color: Colors.red),
                                              ),
                                            );
                                          },
                                        ),
                                      ),
                                    ],
                                  ),
                                ),
                              ],
                              
                              const SizedBox(height: 32),
                              OutlinedButton.icon(
                                onPressed: () {
                                  Navigator.of(context).pop();
                                },
                                icon: const Icon(Icons.arrow_back),
                                label: const Text('Return to Mortal Realm'),
                                style: OutlinedButton.styleFrom(
                                  foregroundColor: _isRealFlag ? const Color(0xFF08CB00) : Colors.orange,
                                  side: BorderSide(color: _isRealFlag ? const Color(0xFF08CB00) : Colors.orange),
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
              );
            },
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
    final width = MediaQuery.of(context).size.width;
    final horizontalPadding = width < 360 ? 16.0 : width < 800 ? 24.0 : 40.0;

    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [
              Color(0xFF000000),
              Color(0xFF253900),
              Color(0xFF000000),
            ],
          ),
        ),
        child: SafeArea(
          child: SingleChildScrollView(
            padding: EdgeInsets.symmetric(horizontal: horizontalPadding, vertical: 24.0),
            child: Center(
              child: ConstrainedBox(
                constraints: const BoxConstraints(maxWidth: 640),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                // Back button
                IconButton(
                  onPressed: () {
                    Navigator.of(context).pop();
                  },
                  icon: const Icon(Icons.arrow_back),
                  color: const Color(0xFF08CB00),
                ),

                const SizedBox(height: 16),

                // Title
                const Text(
                  'The Legend',
                  style: TextStyle(
                    fontSize: 32,
                    fontWeight: FontWeight.bold,
                    color: Color(0xFF08CB00),
                    letterSpacing: 1.5,
                  ),
                ),

                const SizedBox(height: 24),

                // Story content
                const Text(
                  'In Greek mythology, Zeus reigns as the king of all gods, wielder of thunder and lightning. '
                  'He sits atop Mount Olympus, commanding the heavens and earth below.\n\n'
                  'Zeus\'s power is absolute, but even the mighty king of gods has his secrets. '
                  'To access his domain, one must first know how to address him properly.\n\n'
                  'The ancient Greeks knew him by many names, but there is one that grants entry to his realm. '
                  'Once you\'ve identified yourself correctly, you\'ll need to discover the key that unlocks his chamber.\n\n'
                  'The answer lies hidden within his domain - perhaps in the sacred texts, the configuration scrolls, '
                  'or among the artifacts left behind by those who served him.\n\n'
                  'Search carefully through what Zeus has left behind. The key to his kingdom awaits those '
                  'clever enough to look in the right places.\n\n'
                  'Can you gain access to the throne of Olympus?',
                  style: TextStyle(
                    fontSize: 16,
                    color: Color(0xFFEEEEEE),
                    height: 1.8,
                  ),
                ),

                const SizedBox(height: 32),

                Center(
                  child: Container(
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      border: Border.all(color: Color(0xFF08CB00)),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: const Text(
                      'MEDUSA 2.0',
                      style: TextStyle(
                        fontSize: 14,
                        color: Color(0xFF08CB00),
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
      ),
    ),
    );
  }
}
