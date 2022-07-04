// https://szkopul.edu.pl/c/contests/p/szy/
#include <bits/stdc++.h>
using namespace std;

const int N = 1e6 + 5;

int n, m;
char S1[N], S2[N];
int pref[N];
vector<int> indeks[127];
int res;

int find(int c, int ind, int good) {
	int b = 0;
	int e = indeks[c].size() - 1;
	int mid = (b + e) / 2;
	while (b < e) {
		if (indeks[c][mid] > ind) {
			e = mid;
		}
		else {
			b = mid + 1;
		}
		mid = (b + e) / 2;
	}
	if (indeks[c][e] <= ind) {
		res++;
		return find(c, good, 0);
	}
	return indeks[c][b];
}

int main() {
	scanf("%s", &S1);
	scanf("%s", &S2);
	n = strlen(S1);
	m = strlen(S2);
	
	int prefiks = 0;
	for (int i = 2; i <= n; i++) {
		while (prefiks > 0 && S1[prefiks] != S1[i - 1]) {
			prefiks = pref[prefiks];
		}
		if (S1[prefiks] == S1[i - 1]) {
			prefiks++;
		}
		pref[i] = prefiks;
	}
	for (int i = 0; i < n; i++) {
		indeks[S1[i]].push_back(i);
	}
	int gdzie = -1;
	for (int i = 0; i < m; i++) {
		if (indeks[S2[i]].empty()) {
			printf("INF\n");
			return 0;
		}
//		cout << gdzie << endl;
		gdzie = find(S2[i], gdzie, pref[n] - 1);
	}
	printf("%d\n", res);
	
		
}
