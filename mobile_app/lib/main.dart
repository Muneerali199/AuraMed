import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:auramed_mobile/screens/home_screen.dart';
import 'package:auramed_mobile/providers/agent_provider.dart';
import 'package:auramed_mobile/providers/transcript_provider.dart';
import 'package:auramed_mobile/providers/analysis_provider.dart';
import 'package:auramed_mobile/theme/app_theme.dart';

void main() {
  runApp(const AuraMedApp());
}

class AuraMedApp extends StatelessWidget {
  const AuraMedApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AgentProvider()),
        ChangeNotifierProvider(create: (_) => TranscriptProvider()),
        ChangeNotifierProvider(create: (_) => AnalysisProvider()),
      ],
      child: MaterialApp(
        title: 'AuraMed Clinical Co-Pilot',
        theme: AppTheme.lightTheme,
        darkTheme: AppTheme.darkTheme,
        themeMode: ThemeMode.light,
        debugShowCheckedModeBanner: false,
        home: const HomeScreen(),
      ),
    );
  }
}