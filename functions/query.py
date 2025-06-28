import requests
from datetime import datetime
from functions.utils import get_logger, Config

logger = get_logger(__name__)


class ElecRoomQuery:
    """
    Class for querying dormitory water, electricity, and air conditioner balances.
    """

    def __init__(self):
        """
        Initializes the required settings for querying the API, including the bearer token for authentication.
        """
        self.base_url = "https://ecardwxnew.scut.edu.cn"
        self._bearer_token = Config.get("BEARER_TOKEN")

        if not self._bearer_token:
            raise ValueError(
                "Bearer token is missing! Please check your environment variables."
            )

        self._headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Host": "ecardwxnew.scut.edu.cn",
            "Referer": "https://ecardwxnew.scut.edu.cn/plat/shouyeUser",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/107.0.5304.110 Safari/537.36 "
                "Language/zh ColorScheme/Light wxwork/4.1.32 (MicroMessenger/6.2) "
                "WindowsWechat MailPlugin_Electron WeMail embeddisk wwmver/3.26.15.675"
            ),
            "synAccessSource": "wechat-work",
            "synjones-auth": f"Bearer {self._bearer_token}",
        }

    def _query_balance_by_type(self, fee_item_id):
        """
        Internal method to query a specific balance type.

        :param fee_item_id: ID representing the balance type:
                            1 - Electricity
                            2 - Air Conditioner
                            3 - Water
        :return: Raw response data with balance information for the given type.
        """
        endpoint = f"/charge/feeitem/getThirdDataByFeeItemId?feeitemid={fee_item_id}&synAccessSource=wechat-work"
        url = self.base_url + endpoint

        try:
            response = requests.get(url, headers=self._headers)
            response.raise_for_status()
            response_data = response.json()

            logger.debug(f"Query response (fee_item_id={fee_item_id}): {response_data}")
            return response_data.get("map", {}).get("showData", "")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error querying balance for fee_item_id {fee_item_id}: {e}")
            raise ValueError(
                f"Failed to query balance for fee_item_id {fee_item_id}. Error: {e}"
            )

    def query_balance(self):
        """
        Queries balances for electricity, air conditioner, and water, and formats the results into a structured dictionary.

        :return: A dictionary containing the queried balance values and the current timestamp.
        """
        try:
            # Query each balance type
            electricity_data = self._query_balance_by_type(fee_item_id=1)
            air_conditioner_data = self._query_balance_by_type(fee_item_id=2)
            water_data = self._query_balance_by_type(fee_item_id=3)

            # Format and sanitize response data
            balance_info = {
                "timestamp": datetime.now().isoformat(),
                "electricity_balance": self._extract_balance(
                    electricity_data, "房间当前剩余电量"
                ),
                "air_conditioner_balance": self._extract_balance(
                    air_conditioner_data, "房间当前剩余金额"
                ),
                "water_balance": self._extract_balance(
                    water_data, "剩余水费", extract_last=True
                ),
            }

            logger.info(f"Successfully queried balances: {balance_info}")
            return balance_info
        except Exception as e:
            logger.error(f"Failed to query all balances: {e}")
            return None

    def _extract_balance(self, raw_data, prefix, extract_last=False):
        """
        Extracts and sanitizes balance data from raw query results.

        :param raw_data: String containing raw text data from the query response.
        :param prefix: Prefix to remove from the raw data (e.g., "房间当前剩余电量").
        :param extract_last: If True, extract and return the last part of the string after splitting by ','.
        :return: A sanitized float value representing the balance.
        """
        try:
            sanitized_data = raw_data.replace(prefix, "").strip()
            if extract_last:  # Special handling for water balance
                sanitized_data = sanitized_data.split(",")[-1].strip()
            return float(sanitized_data)
        except ValueError as e:
            logger.error(f"Error extracting balance from data '{raw_data}': {e}")
            return 0.0
