/* ===================== pubspec.yaml (info) =====================
name: tabbo_info
description: One-file OSINT tool with AdMob
environment:
  sdk: ">=2.19.0 <3.0.0"

dependencies:
  flutter:
    sdk: flutter
  http: ^1.2.0
  google_mobile_ads: ^3.0.0

flutter:
  uses-material-design: true
================================================================*/

import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:google_mobile_ads/google_mobile_ads.dart';

// CONFIG ---------------------------------------------------------------------
class K {
  static const neon = Color(0xFF00FF41);
  static const appName = 'Tabbo Info';

  // AdMob
  static const appId      = 'ca-app-pub-4599007752383978~1349246853';
  static const bannerId   = 'ca-app-pub-4599007752383978/7049130242';
  static const rewardedId = 'ca-app-pub-4599007752383978/1793041934';

  // APIs
  static const p = {
    'number':'https://splexxo123-7saw.vercel.app/api/seller?mobile=',
    'aadhaar':'https://aadharinfo.gauravcyber0.workers.dev/?aadhar=',
    'vehicle':'https://vechil-pro-ng.vercel.app/?vc=',
    'rc'     :'https://vvvin-ng.vercel.app/lookup?rc=',
    'imei'   :'https://ng-imei-info.vercel.app/?imei_num=',
    'family' :'http://india.42web.io/family/?q=',
    'gst'    :'https://gstlookup.hideme.eu.org/?gstNumber=',
  };

  // Backup API
  static const b = {
    'number':'http://india.42web.io/number.php?q=',
    'vehicle':'http://india.42web.io/vehicle/?q=',
  };

  static const splexxoKey = '&key=SPLEXXO';
}

// ADS ------------------------------------------------------------------------
class Ads {
  static late BannerAd banner;
  static RewardedAd? _rw;

  static Future init() async {
    await MobileAds.instance.initialize();

    banner = BannerAd(
      adUnitId: K.bannerId,
      size: AdSize.banner,
      request: const AdRequest(),
      listener: BannerAdListener(
        onAdFailedToLoad: (_, __) => banner.load(),
      ),
    )..load();

    _loadRw();
  }

  static void _loadRw() => RewardedAd.load(
        adUnitId: K.rewardedId,
        request: const AdRequest(),
        rewardedAdLoadCallback: RewardedAdLoadCallback(
          onAdLoaded: (ad) => _rw = ad,
          onAdFailedToLoad: (_) => _rw = null,
        ),
      );

  static void showRw() {
    if (_rw == null) return;

    _rw!.fullScreenContentCallback = FullScreenContentCallback(
      onAdDismissedFullScreenContent: (_) => _loadRw(),
      onAdFailedToShowFullScreenContent: (_, __) => _loadRw(),
    );

    _rw!.show(onUserEarnedReward: (_, __) {});
    _rw = null;
  }
}

// TOOLS ----------------------------------------------------------------------
class Tool {
  final String k, t, h;
  final IconData i;

  const Tool(this.k, this.t, this.i, this.h);
}

const tools = [
  Tool('number', 'Number', Icons.phone_android, '10-digit number'),
  Tool('aadhaar', 'Aadhaar', Icons.credit_card, '12-digit Aadhaar'),
  Tool('family', 'Family', Icons.people, 'Aadhaar again'),
  Tool('vehicle', 'Vehicle', Icons.directions_car, 'MH12DE1433'),
  Tool('rc', 'RC Lookup', Icons.directions_car_filled, 'RC Number'),
  Tool('imei', 'IMEI', Icons.devices_other, '15-digit IMEI'),
  Tool('gst', 'GST', Icons.business, 'GSTIN'),
];

// APP MAIN -------------------------------------------------------------------
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Ads.init();
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(_) => MaterialApp(
        debugShowCheckedModeBanner: false,
        title: K.appName,
        theme: ThemeData.dark().copyWith(
          scaffoldBackgroundColor: const Color(0xFF001500),
          elevatedButtonTheme: ElevatedButtonThemeData(
            style: ElevatedButton.styleFrom(
              backgroundColor: K.neon,
              foregroundColor: Colors.black,
            ),
          ),
        ),
        routes: {
          '/': (_) => const Disc(),
          '/h': (_) => const Home(),
          '/s': (_) => const Search(),
        },
      );
}

// DISCLAIMER PAGE -------------------------------------------------------------
class Disc extends StatelessWidget {
  const Disc({super.key});

  @override
  Widget build(c) => Scaffold(
        body: Center(
          child: Padding(
            padding: const EdgeInsets.all(24),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(
                  'DISCLAIMER',
                  style: TextStyle(
                    fontSize: 28,
                    color: K.neon,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 16),
                const Text(
                  'Educational / OSINT purposes only.',
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 25),
                ElevatedButton(
                  onPressed: () => Navigator.pushReplacementNamed(c, '/h'),
                  child: const Text('CONTINUE'),
                ),
              ],
            ),
          ),
        ),
      );
}

// HOME -----------------------------------------------------------------------
class Home extends StatelessWidget {
  const Home({super.key});

  @override
  Widget build(c) => Scaffold(
        appBar: AppBar(title: Text(K.appName)),
        body: Column(
          children: [
            Expanded(
              child: ListView(
                padding: const EdgeInsets.all(12),
                children: tools
                    .map(
                      (t) => Card(
                        color: Colors.black54,
                        child: ListTile(
                          leading: Icon(t.i, color: K.neon),
                          title: Text(
                            t.t,
                            style: const TextStyle(
                                fontSize: 18, fontWeight: FontWeight.bold),
                          ),
                          trailing: const Icon(Icons.arrow_forward_ios,
                              size: 16, color: K.neon),
                          onTap: () =>
                              Navigator.pushNamed(c, '/s', arguments: t),
                        ),
                      ),
                    )
                    .toList(),
              ),
            ),
            SizedBox(height: 52, child: AdWidget(ad: Ads.banner)),
          ],
        ),
      );
}

// SEARCH PAGE ----------------------------------------------------------------
class Search extends StatefulWidget {
  const Search({super.key});
  @override
  _S createState() => _S();
}

class _S extends State<Search> {
  late Tool tool;
  final _c = TextEditingController();
  bool load = false;
  dynamic res;
  String? err;

  @override
  void didChangeDependencies() {
    tool = ModalRoute.of(context)!.settings.arguments as Tool;
    super.didChangeDependencies();
  }

  Uri _u(Map<String, String> m, String q) {
    var url = m[tool.k] ?? '';
    if (url.isEmpty) return Uri();

    if (tool.k == 'number' && url.contains('splexxo')) {
      url += K.splexxoKey;
    }

    return Uri.parse('$url$q');
  }

  Future<bool> _hit(Uri u) async {
    if (u.scheme.isEmpty) return false;

    try {
      final r = await http.get(u).timeout(const Duration(seconds: 10));
      if (r.statusCode == 200) {
        res = jsonDecode(r.body);
        return true;
      }
    } catch (_) {}

    return false;
  }

  Future<void> _go() async {
    setState(() {
      load = true;
      err = null;
      res = null;
    });

    final q = _c.text.trim();

    bool ok = await _hit(_u(K.p, q));
    if (!ok) ok = await _hit(_u(K.b, q));

    if (ok)
      Ads.showRw();
    else
      err = 'Both servers failed';

    setState(() => load = false);
  }

  @override
  Widget build(c) => Scaffold(
        appBar: AppBar(title: Text(tool.t)),
        body: SingleChildScrollView(
          padding: const EdgeInsets.all(20),
          child: Column(
            children: [
              TextField(
                  controller: _c,
                  decoration: InputDecoration(
                      filled: true, hintText: tool.h)),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: load ? null : _go,
                child: load
                    ? const CircularProgressIndicator()
                    : const Text('SEARCH'),
              ),
              const SizedBox(height: 20),
              if (err != null)
                Text(err!, style: const TextStyle(color: Colors.red)),
              if (res != null)
                Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(14),
                  decoration: BoxDecoration(
                      color: Colors.black54,
                      borderRadius: BorderRadius.circular(6)),
                  child: Text(
                    const JsonEncoder.withIndent('  ').convert(res),
                    style: TextStyle(
                      fontFamily: 'Courier',
                      color: K.neon,
                    ),
                  ),
                ),
              const SizedBox(height: 20),
              SizedBox(height: 52, child: AdWidget(ad: Ads.banner)),
            ],
          ),
        ),
      );
}
