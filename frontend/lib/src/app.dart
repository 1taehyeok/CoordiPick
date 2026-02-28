import 'package:flutter/material.dart';

import 'screens/admin_screen.dart';
import 'screens/start_screen.dart';

class CoordiPickApp extends StatelessWidget {
  const CoordiPickApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'CoordiPick',
      theme: ThemeData(useMaterial3: true, colorSchemeSeed: Colors.teal),
      home: const _RootScreen(),
    );
  }
}

class _RootScreen extends StatelessWidget {
  const _RootScreen();

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 2,
      child: Scaffold(
        appBar: AppBar(
          title: const Text('CoordiPick Frontend'),
          bottom: const TabBar(
            tabs: [
              Tab(text: 'User'),
              Tab(text: 'Admin'),
            ],
          ),
        ),
        body: const TabBarView(
          children: [
            StartScreen(),
            AdminScreen(),
          ],
        ),
      ),
    );
  }
}