#include <bits/stdc++.h>
using namespace std;

const int N = 5e5 + 5;

int n, m;
int tab[N];
vector<int> number[N];

int get_less(int gdzie, int x) {
	if (number[x][0] > gdzie)	return 0;
	int l = 0, r = number[x].size() - 1;
	int mid = (l + r) / 2 + 1;
	while (l < r) {
		if (number[x][mid] <= gdzie) {
			l = mid;
		}
		else {
			r = mid - 1;
		}
		mid = (l + r) / 2 + 1;
	}
	return l + 1;
}
			

int get_amount(int l, int r, int x) {
	return get_less(r, x) - get_less(l - 1, x);
}

const long long mod = 1e9 + 7;	

int main()
{
	srand(time(NULL));
	scanf("%d%d", &n, &m);
	for (int i = 1; i <= n; i++) {
		scanf("%d", &tab[i]);
	}
	for (int i = 1; i <= n; i++) {
		number[tab[i]].push_back(i);
	}
	while (m--) {
		int a, b;
		scanf("%d%d", &a, &b);
		bool ok = false;
		for (int i = 0; i < 30; i++) {
			int c = rand() % (b -a + 1) + a;
			if (get_amount(a, b, tab[c]) > (b - a + 1) / 2) {
				printf("%d\n", tab[c]);
				ok = true;
				break;
			}
		}
		if (!ok) {
			printf("0\n");
		}
	}
				
}
